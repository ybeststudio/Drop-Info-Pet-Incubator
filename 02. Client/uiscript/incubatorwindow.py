# File Name : incubatorwindow.py
# Author    : BestStudio
# Version   : 1.0
# Date      : 2026-11-13
#
# header_bg 6,28 / background_bg 6,56 / desc_name_bg 0,7 / name_bg 0,32 / name 10,3 / confirm_btn 0,58 (135x25).
import localeInfo

WIDTH = 215
HEIGHT = 160
INCUBATOR = "d:/ymir work/ui/game/companion/incubator/"
LABEL = (202.0 / 255.0, 189.0 / 255.0, 171.0 / 255.0)

window = {
	"name" : "PetHatchingWindow",
	"style" : ("movable", "float",),
	"x" : SCREEN_WIDTH / 2 - WIDTH / 2,
	"y" : SCREEN_HEIGHT / 2 - HEIGHT / 2,
	"width" : WIDTH,
	"height" : HEIGHT,
	"children" :
	(
		{
			"name" : "PetHatching_TitleBar",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : WIDTH,
			"height" : HEIGHT,
			"title" : localeInfo.PET_INCUBATOR_TITLE,
			"children" :
			(
				{
					"name" : "header_bg", "type" : "expanded_image", "style" : ("not_pick",),
					"x" : 6, "y" : 28, "image" : INCUBATOR + "header_bg.png",
					"children" :
					(
						{ "name" : "header", "type" : "text", "x" : 101, "y" : 9, "text" : localeInfo.PET_INCUBATOR_HEADER,
						  "fontname" : "Tahoma:12b", "text_horizontal_align" : "center", "r" : LABEL[0], "g" : LABEL[1], "b" : LABEL[2], "a" : 1.0, },
					),
				},
				{
					"name" : "background_bg", "type" : "expanded_image",
					"x" : 6, "y" : 56, "image" : INCUBATOR + "background.png",
					"children" :
					(
						{
							"name" : "desc_name_bg", "type" : "expanded_image", "style" : ("not_pick",),
							"x" : 9, "y" : 7, "image" : INCUBATOR + "desc_bg.png",
							"children" :
							(
								{ "name" : "HatchingMoney", "type" : "text", "x" : 92, "y" : 3, "text" : "",
								  "text_horizontal_align" : "center", "r" : LABEL[0], "g" : LABEL[1], "b" : LABEL[2], "a" : 1.0, },
							),
						},
						{
							"name" : "name_bg", "type" : "expanded_image",
							"x" : 9, "y" : 32, "image" : INCUBATOR + "editline_bg.png",
							"children" :
							(
								{ "name" : "pet_name", "type" : "editline", "x" : 10, "y" : 3, "width" : 164, "height" : 15,
								  "input_limit" : 20, "info_msg" : localeInfo.PET_INCUBATOR_ENTER_NAME, },
							),
						},
						{
							"name" : "HatchingButton", "type" : "button",
							"x" : 33, "y" : 58,
							"text" : localeInfo.PET_INCUBATOR_CONFIRM,
							"default_image" : INCUBATOR + "btn_norm.png",
							"over_image" : INCUBATOR + "btn_hover.png",
							"down_image" : INCUBATOR + "btn_select.png",
						},
					),
				},
				# kept for uipetinfo (egg vnum holder), never shown
				{
					"name" : "HatchingItemSlot", "type" : "slot",
					"x" : 0, "y" : 0, "width" : 32, "height" : 32,
					"slot" : ({"index" : 0, "x" : 0, "y" : 0, "width" : 32, "height" : 32},),
				},
			),
		},
	),
}
