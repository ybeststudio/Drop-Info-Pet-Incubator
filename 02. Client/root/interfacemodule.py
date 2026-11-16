# Ara:
import uiRestart
import uiToolTip

# Altina ekle:
import uidropinfo


# Interface.__init__ icinde ara:
		if app.ENABLE_VIEW_CHEST_DROP:
			self.dlgChestDrop = None

# Altina ekle:
		self.dlgDropInfo = None


# Interface.__MakeWindows icinde ara:
		if app.ENABLE_VIEW_CHEST_DROP:
			self.dlgChestDrop = uiChestDrop.ChestDropWindow()

# Altina ekle:
		self.dlgDropInfo = uidropinfo.DropInfoWindow()


# Interface.Close icinde ara:
			if self.dlgChestDrop:
				self.dlgChestDrop.Destroy()

# Altina ekle:
		if self.dlgDropInfo:
			self.dlgDropInfo.Destroy()


# Interface.Close icinde ara:
			if self.dlgChestDrop:
				del self.dlgChestDrop

# Altina ekle:
		if self.dlgDropInfo:
			del self.dlgDropInfo


# Interface.__CheckDropYang icinde ara:
		last = self._dropInfoGold
		self._dropInfoGold = gold

# Altina ekle:
		if last is None or gold <= last or self.dlgDropInfo is None:
			return


# Interface.__CheckDropYang icinde ara:
		import advanced_options_runtime
		if advanced_options_runtime.Get("view_drop_ui", True):

# Altina ekle:
			self.dlgDropInfo.AppendYang(gold - last)


# Interface.__CheckNewDropItems icinde ara:
	def __CheckNewDropItems(self):
		return

# Altina ekle:
		if self.dlgDropInfo is None:
			return


# Interface.__CheckNewDropItems icinde ara:
			oldEntry = previous.get(slot)
			if oldEntry is None:

# Altina ekle:
				self.dlgDropInfo.AppendDropInfo(vnum, count)


# Interface.__CheckNewDropItems icinde ara:
			elif oldEntry[0] == vnum and count > oldEntry[1]:

# Altina ekle:
				self.dlgDropInfo.AppendDropInfo(vnum, count - oldEntry[1])


# Interface.__CheckNewDropItems icinde ara:
			elif oldEntry[0] != vnum:

# Altina ekle:
				self.dlgDropInfo.AppendDropInfo(vnum, count)


# Interface.SpecialChatOnPick icinde ara:
		def SpecialChatOnPick(self, money = 0, item_vnum = 0, socket0 = 0):

# Altina ekle:
			if self.dlgDropInfo:
				if money > 0:
					self.dlgDropInfo.AppendYang(money)
				if item_vnum > 0:
					self.dlgDropInfo.AppendDropInfo(item_vnum, 1, socket0)
				return

