#
# File Name : uidropinfo.py
# Author    : BestStudio
# Version   : 2.0
# Date      : 2026-11-13
#
# (dropinfo_probe.json: 205x326 board at 10,138, rectWindow 0,15 205x282, scroll bar 190,13 5x301,
# GAP 12, name grey, count yellow (YELLOW_COLOR), OPEN_TIME 25 s, MAX_DROP_ENTRIES 20.
import ui
import wndMgr
import app
import item
import skill
if __USE_DYNAMIC_MODULE__:
	import pyapi
player = __import__(pyapi.GetModuleName("player"))
import localeInfo
import uiToolTip

DROP_PATH = "d:/ymir work/ui/game/dropinfo/%s"
BOARD_SIZE = (205, 326)
BOARD_POS = (10, 138)
RECT_POS = (0, 15)
RECT_SIZE = (205, 282)
MAX_DROP_ENTRIES = 20
OPEN_TIME = 25.0
FADE_DURATION = 0.3
GAP = 12
SLOT_X = 12
NAME_X = 44
FIRST_TOP = 12 - RECT_POS[1]		# first slot top inside rectWindow (window y 12)
SCROLL_STEP = 22
YANG_VNUM = 1

NAME_COLOR = 0xffc1c1c1		# uiDropInfo NORMAL_COLOR (0.7607)
COUNT_COLOR = 0xffffc800	# uiDropInfo YELLOW_COLOR (1.0, 0.7843, 0.0)
HINT_COLOR = 0xffd7c9aa		# measured


class DropScrollBar(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.pos = 0.0
		self.middleScale = 1.0
		self.event = None
		self.wheelEvent = None
		self.dragging = False
		self.frame = []
		for i in xrange(4):
			bar = ui.Bar()
			bar.SetParent(self)
			bar.SetColor(0xff565656)
			bar.AddFlag("not_pick")
			bar.Show()
			self.frame.append(bar)
		self.middle = ui.Bar()
		self.middle.SetParent(self)
		self.middle.SetColor(0xff8a8a8a)
		self.middle.AddFlag("not_pick")
		self.middle.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def SetScrollBarSize(self, height):
		self.SetSize(5, height)
		(l, t, r, b) = self.frame
		l.SetPosition(0, 0)
		l.SetSize(1, height)
		r.SetPosition(4, 0)
		r.SetSize(1, height)
		t.SetPosition(1, 0)
		t.SetSize(3, 1)
		b.SetPosition(1, height - 1)
		b.SetSize(3, 1)
		self.__Refresh()

	def SetMiddleBarSize(self, scale):
		self.middleScale = max(0.05, min(1.0, scale))
		self.__Refresh()

	def SetScrollEvent(self, event):
		self.event = event

	def GetPos(self):
		return self.pos

	def SetPos(self, pos):
		self.pos = max(0.0, min(1.0, pos))
		self.__Refresh()
		if self.event:
			self.event()

	def __Refresh(self):
		height = self.GetHeight()
		barH = max(8, int((height - 2) * self.middleScale))
		self.middle.SetSize(3, barH)
		self.middle.SetPosition(1, 1 + int((height - 2 - barH) * self.pos))

	def __PosFromMouse(self):
		(x, y) = self.GetMouseLocalPosition()
		barH = max(8, int((self.GetHeight() - 2) * self.middleScale))
		span = max(1, self.GetHeight() - 2 - barH)
		self.SetPos(float(y - 1 - barH / 2) / span)

	def OnMouseLeftButtonDown(self):
		self.dragging = True
		self.__PosFromMouse()

	def OnMouseLeftButtonUp(self):
		self.dragging = False

	def OnUpdate(self):
		if self.dragging:
			self.__PosFromMouse()

	def OnRunMouseWheel(self, delta):
		if self.wheelEvent:
			return self.wheelEvent(delta)
		return True


class DropInfoWindow(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self)
		self.entries = []		# newest first: {"vnum", "count", "text", "widgets"}
		self.tooltipItem = None
		self.endTime = 0.0
		self.fadeStart = 0.0
		self.scrollOffset = 0
		self.CreateWindow()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def CreateWindow(self):
		self.SetWindowName("DropInfoWindow")
		self.SetSize(BOARD_SIZE[0], BOARD_SIZE[1])
		self.SetPosition(BOARD_POS[0], BOARD_POS[1])

		rect = ui.Window()
		rect.SetParent(self)
		rect.SetPosition(RECT_POS[0], RECT_POS[1])
		rect.SetSize(RECT_SIZE[0], RECT_SIZE[1])
		rect.Show()
		self.rectWindow = rect

		scroll = DropScrollBar()
		scroll.SetParent(self)
		scroll.SetPosition(190, 13)
		scroll.SetScrollBarSize(301)
		scroll.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scroll.wheelEvent = ui.__mem_func__(self.OnRunMouseWheel)
		scroll.Hide()
		self.scrollBar = scroll

		key = ui.ImageBox()
		key.SetParent(self)
		key.LoadImage("icon/emoji/key/tab.png")
		key.SetPosition(52, 306)
		key.AddFlag("not_pick")
		key.Show()
		self.tabKey = key
		hint = ui.TextLine()
		hint.SetParent(self)
		hint.SetPosition(93, 307)
		hint.SetPackedFontColor(HINT_COLOR)
		hint.SetOutline()
		hint.SetText(localeInfo.DROP_INFO_TAB_HINT)
		hint.Show()
		self.tabHint = hint

		self.Hide()

	def Destroy(self):
		self.__ClearWidgets()
		self.entries = []
		self.tooltipItem = None

	def Open(self):
		self.Show()

	def Close(self):
		self.Hide()

	# ------------------------------------------------------------------ entries
	def AppendDropInfo(self, itemVnum, itemCount = 1, socket0 = 0):
		itemVnum = int(itemVnum)
		itemCount = max(1, int(itemCount))
		socket0 = int(socket0)
		now = app.GetTime()
		if self.entries and self.entries[0]["vnum"] == itemVnum and self.entries[0].get("socket0", 0) == socket0 and now - self.entries[0].get("time", 0) < 1.0 and itemVnum != YANG_VNUM:
			entry = self.entries[0]
			entry["count"] += itemCount
			entry["text"] = localeInfo.DROP_INFO_COUNT % entry["count"]
			entry["time"] = now
			self.__Rebuild()
			self.endTime = now + OPEN_TIME
			return
		entry = {"vnum": itemVnum, "count": itemCount, "text": localeInfo.DROP_INFO_COUNT % itemCount, "time": now, "socket0": socket0}
		bookName = self.__SkillBookName(itemVnum, socket0)
		if bookName:
			entry["name"] = bookName
		self.__AddEntry(entry)

	def __SkillBookName(self, itemVnum, socket0):
		if not socket0:
			return ""
		item.SelectItem(itemVnum)
		if item.GetItemType() != item.ITEM_TYPE_SKILLBOOK and itemVnum not in (70037, 70055):
			return ""
		try:
			skillName = skill.GetSkillName(socket0)
		except:
			return ""
		if not skillName:
			return ""
		bookName = localeInfo.TOOLTIP_SKILLBOOK_NAME if item.GetItemType() == item.ITEM_TYPE_SKILLBOOK else localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME
		return skillName + " " + bookName

	def AppendYang(self, amount):
		self.__AddEntry({"vnum": YANG_VNUM, "count": amount, "text": localeInfo.DROP_INFO_YANG % localeInfo.MoneyFormat(amount), "name": localeInfo.DROP_INFO_YANG_NAME})

	def AppendShopSold(self, itemVnum):
		item.SelectItem(int(itemVnum))
		self.__AddEntry({"vnum": int(itemVnum), "count": 0, "name": item.GetItemName(), "text": localeInfo.DROP_INFO_SHOP_SOLD % item.GetItemName()})

	def AppendChatInfo(self, text):
		self.__AddEntry({"vnum": 0, "count": 0, "text": text})

	def __AddEntry(self, entry):
		self.entries.insert(0, entry)
		del self.entries[MAX_DROP_ENTRIES:]
		self.scrollOffset = 0
		self.scrollBar.SetPos(0.0)
		self.__Rebuild()
		self.endTime = app.GetTime() + OPEN_TIME
		self.fadeStart = 0.0
		import advanced_options_runtime
		if advanced_options_runtime.Get("view_drop_ui", True):
			self.Show()
			self.SetTop()

	def __ClearWidgets(self):
		for entry in self.entries:
			for w in entry.get("widgets", []):
				w.Hide()
			entry["widgets"] = []

	def __SlotHeight(self, vnum):
		if not vnum:
			return 32
		item.SelectItem(vnum)
		return 32 * max(1, min(3, item.GetItemSize()[1]))

	def __ContentHeight(self):
		h = FIRST_TOP
		for entry in self.entries:
			h += self.__SlotHeight(entry["vnum"]) + GAP
		return h

	def __Clip(self, w):
		if app.ENABLE_CLIP_MASKING:
			w.SetClippingMaskWindow(self.rectWindow)

	def __Image(self, path, x, y):
		img = ui.ImageBox()
		img.SetParent(self.rectWindow)
		img.LoadImage(path)
		img.SetPosition(x, y)
		img.AddFlag("not_pick")
		self.__Clip(img)
		img.Show()
		return img

	def __Text(self, text, x, y, color):
		line = ui.TextLine()
		line.SetParent(self.rectWindow)
		line.SetPosition(x, y)
		line.SetPackedFontColor(color)
		line.SetOutline()
		line.SetText(text)
		self.__Clip(line)
		line.Show()
		return line

	def __Rebuild(self):
		self.__ClearWidgets()
		content = self.__ContentHeight()
		overflow = max(0, content - RECT_SIZE[1])
		if overflow > 0:
			self.scrollBar.SetMiddleBarSize(float(RECT_SIZE[1]) / content)
			self.scrollBar.Show()
		else:
			self.scrollBar.Hide()
		self.scrollOffset = min(self.scrollOffset, overflow)

		top = FIRST_TOP - self.scrollOffset
		for index, entry in enumerate(self.entries):
			height = self.__SlotHeight(entry["vnum"])
			widgets = []
			if top + height > -GAP and top - 13 < RECT_SIZE[1]:
				slotName = "slot_%d.tga" % (height / 32)
				widgets.append(self.__Image(DROP_PATH % slotName, SLOT_X, top))
				if entry["vnum"]:
					item.SelectItem(entry["vnum"])
					icon = ui.ImageBox()
					icon.SetParent(self.rectWindow)
					icon.LoadImage(item.GetIconImageFileName())
					icon.SetPosition(SLOT_X, top)
					icon.SetStringEvent("MOUSE_OVER_IN", lambda i = index: self.OverInItem(i))
					icon.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.OverOutItem))
					self.__Clip(icon)
					icon.Show()
					widgets.append(icon)
					name = entry.get("name") or item.GetItemName()
				else:
					name = entry.get("name", "")
				widgets.append(self.__Image(DROP_PATH % "name.tga", NAME_X, top - 13))
				widgets.append(self.__Text(name, NAME_X + 5, top - 2, NAME_COLOR))
				widgets.append(self.__Image(DROP_PATH % "line.tga", NAME_X, top + 13))
				widgets.append(self.__Text(entry["text"], NAME_X + 5, top + 15, COUNT_COLOR))
			entry["widgets"] = widgets
			top += height + GAP

	def __OnScroll(self):
		overflow = max(0, self.__ContentHeight() - RECT_SIZE[1])
		self.scrollOffset = int(overflow * self.scrollBar.GetPos())
		self.__Rebuild()
		self.endTime = app.GetTime() + OPEN_TIME

	def OnRunMouseWheel(self, delta):
		overflow = max(0, self.__ContentHeight() - RECT_SIZE[1])
		if not overflow:
			return True
		step = SCROLL_STEP if delta < 0 else -SCROLL_STEP
		self.scrollBar.SetPos(float(max(0, min(overflow, self.scrollOffset + step))) / overflow)
		return True

	# ------------------------------------------------------------------ tooltip
	def OverInItem(self, index):
		if not (0 <= index < len(self.entries)) or not self.entries[index]["vnum"]:
			return
		if self.tooltipItem is None:
			self.tooltipItem = uiToolTip.ItemToolTip()
		entry = self.entries[index]
		if entry.get("socket0", 0):
			metinSlot = [entry["socket0"]] + [0] * (player.METIN_SOCKET_MAX_NUM - 1)
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(entry["vnum"], metinSlot)
			self.tooltipItem.ShowToolTip()
		else:
			self.tooltipItem.SetItemToolTip(entry["vnum"])
		self.endTime = app.GetTime() + OPEN_TIME

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnWarping(self):
		self.__ClearWidgets()
		self.entries = []
		self.OverOutItem()
		self.Hide()

	def OnUpdate(self):
		if not self.entries or not self.endTime:
			return
		now = app.GetTime()
		if self.IsIn():
			self.endTime = now + OPEN_TIME
			return
		if now >= self.endTime:
			if not self.fadeStart:
				self.fadeStart = now
			if now - self.fadeStart >= FADE_DURATION:
				self.endTime = 0.0
				self.fadeStart = 0.0
				self.__ClearWidgets()
				self.entries = []
				self.OverOutItem()
				self.Hide()
