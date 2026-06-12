local IsLuaSTGSub = type(lstg.GetVersionNumber) == "function"
local IsLuaSTGPlus = not (IsLuaSTGSub)

local print = lstg and lstg.Print or Print or print
local concat = table.concat
local insert = table.insert
local traceback = debug.traceback
local select = select
local pairs = pairs
local ipairs = ipairs
local tostring = tostring

-- 兼容未来的统一菜单输入

local MenuKeyIsDown = MenuKeyIsDown
local MenuKeyIsPressed = MenuKeyIsPressed
if not MenuKeyIsDown then
    function MenuKeyIsDown(name)
        local code = setting.keysys[name] or setting.keys[name]
        if code then
            return lstg.GetKeyState(code)
        else
            return false
        end
    end
end
if not MenuKeyIsPressed then
    function MenuKeyIsPressed(name)
        local code = setting.keysys[name] or setting.keys[name]
        if code then
            return lstg.GetLastKey() == code
        else
            return false
        end
    end
end

---获取当前代码层级结构
---@return string
local function GetTraceBack()
    return traceback("", 2)
end

---输出日志
local function Log(...)
    local list = { ... }
    for i = 1, select("#", ...) do
        list[i] = tostring(list[i])
    end
    print("[LuaSTG Weekend Extension] " .. concat(list, "\t"))
end

---当前是否已经在处理用户逻辑
---@type boolean
local Processing = false

---当前正在处理的用户名称
---@type string
local CurrentAuthor

---记录的用户顺序
local RecordAuthorList = {}
---当前记录的用户序号
local RecordAuthorIndex = 0

---已记录的编辑器定义列表
local RecordEditorDefinedClass = {}
local RecordAllCardCount = 0
local _original_editor_class = _editor_class
local _original_editor_tasks = _editor_tasks
local _original_sc_table = _sc_table

---判断一个类是否是boss
---@return boolean
local function IsBoss(class)
    if class == boss then
        return true
    elseif class.base
            and class.base ~= object
            and class.base ~= background
            and class.base ~= bullet
            and class.base ~= laser
            and class.base ~= laser_bent
            and class.base ~= item
            and class.base ~= player
    then
        return IsBoss(class.base)
    end
    return false
end

---枚举boss
---@param classes table
---@return table
local function EnumBosses(classes)
    local result = {}
    for k, v in pairs(classes) do
        if IsBoss(v) then
            v._class_name = k
            insert(result, v)
        end
    end
    return result
end

---开始记录编辑器定义类
---@param name string
local function StartRecordingEditorClass(name)
    if not RecordEditorDefinedClass[name] then
        RecordEditorDefinedClass[name] = {
            author = name,
            res = {},
            class = {},
            tasks = {},
            _sc_table = {},
            _sorted_sc_table = {}
        }
    end
    local record = RecordEditorDefinedClass[name]
    _editor_class = record.class
    _editor_tasks = record.tasks
    _sc_table = record._sc_table
end

---结束记录编辑器定义类
---@param name string
local function EditorClassRecordFinish(name)
    local class, tasks, sc = _editor_class, _editor_tasks, _sc_table
    local bosses = EnumBosses(class)
    local _sorted_sc_table = RecordEditorDefinedClass[name]._sorted_sc_table
    local base_sc_list_sorted = {}
    for _, card in ipairs(sc) do
        local c1 = class[card[1]]   -- boss
        local c2 = card[2]          -- 卡名
        local c3 = card[3]          -- 卡
        local c4 = card[4]          -- 编号
        local c5 = card[5]          -- 是否perform
        base_sc_list_sorted[c1] = base_sc_list_sorted[c1] or {}
        insert(base_sc_list_sorted[c1], { c1, c2, c3, c4, c5 })
    end
    for _, boss in ipairs(bosses) do
        local data = {
            name = boss.name,
            card = {},
        }
        if boss.cards then
            local index = 0
            for i, card in ipairs(boss.cards) do
                if card.is_combat then
                    local found_index
                    for bi, v in ipairs(base_sc_list_sorted[boss] or {}) do
                        if v[4] == i then
                            found_index = bi
                            break
                        end
                    end
                    local scp
                    if found_index then
                        scp = {
                            boss._class_name,
                            boss.name,
                            base_sc_list_sorted[boss][found_index][2],
                            card,
                            i,
                            card.perform or base_sc_list_sorted[boss][found_index][5]
                        }
                    else
                        index = index + 1
                        scp = {
                            boss._class_name,
                            boss.name,
                            ("Non-Spellcard #%d - [auto added by extension]"):format(index),
                            card,
                            i,
                            false
                        }
                    end
                    insert(data.card, scp)
					RecordAllCardCount = RecordAllCardCount + 1
                    Log(("Register card to boss %q : %q"):format(boss.name, scp[3]))
                end
            end
        end
        insert(_sorted_sc_table, data)
    end
    _editor_class = _original_editor_class
    _editor_tasks = _original_editor_tasks
    _sc_table = _original_sc_table
    for k, v in pairs(class) do
        if _editor_class[k] then
            Log(("发现 %q 的工程内编辑器定义与其他人的定义存在重名 class : %q"):format(name, k))
        end
        _editor_class[k] = v
    end
    for k, v in pairs(tasks) do
        if _editor_tasks[k] then
            Log(("发现 %q 的工程内编辑器定义与其他人的定义存在重名 task : %q"):format(name, k))
        end
        _editor_tasks[k] = v
    end
    for k, v in ipairs(sc) do
        insert(_sc_table, v)
    end
end

---执行加载子工程前的处理逻辑
---@param name string
function BeforeLoadSubProject(name)
    if Processing then
        Log(("在未声明结束当前正在处理的工程的情况下开始了对 %q 的工程的处理"):format(name))
    end
    CurrentAuthor = name
    RecordAuthorIndex = RecordAuthorIndex + 1
    RecordAuthorList[name] = RecordAuthorIndex
    RecordAuthorList[RecordAuthorIndex] = name
    Processing = true
    StartRecordingEditorClass(name)
    Log(("开始处理 %q 的工程"):format(name))
end

---执行加载子工程后的处理逻辑
---@param name string
function AfterLoadSubProject(name)
    if not (Processing) then
        Log(("在未声明进行处理的情况下结束了对 %q 的工程的处理"):format(name))
    end
    EditorClassRecordFinish(name)
    Log(("%q 的工程处理完毕"):format(name))
    CurrentAuthor = nil
    Processing = false
end

local NonString = "---"
local renderTTF = function(text, x, y, a, r, g, b)
    RenderTTF("sc_pr", text, x, x, y, y, Color(a, r, g, b), "centerpoint")
end
local renderTTFL = function(text, x, y, a, r, g, b)
    RenderTTF("sc_pr", text, x, x, y, y, Color(a, r, g, b), "vcenter", "left")
end
local renderTTFR = function(text, x, y, a, r, g, b)
    RenderTTF("sc_pr", text, x, x, y, y, Color(a, r, g, b), "vcenter", "right")
end
---绘制一个矩形
---@param left number @矩形左边
---@param right number @矩形右边
---@param bottom number @矩形底边
---@param top number @矩形顶边
---@param color Color|table @矩形颜色，单Color指定为单色，table则指定为四个顶点各自的颜色
local renderRect = function(left, right, bottom, top, color)
	if type(color) == 'table' then
		SetImageState("white", '', color[1], color[2], color[3], color[4])
	else
		SetImageState("white", '', color)
	end
	RenderRect("white", left, right, bottom, top)
end
---打印表
function table.print ( t )  
    local print_r_cache={}
    local function sub_print_r(t,indent)
        if (print_r_cache[tostring(t)]) then
            Print(indent.."*"..tostring(t))
        else
            print_r_cache[tostring(t)]=true
            if (type(t)=="table") then
                for pos,val in pairs(t) do
                    if (type(val)=="table") then
                        Print(indent.."["..pos.."] => "..tostring(t).." {")
                        sub_print_r(val,indent..string.rep(" ",string.len(pos)+8))
                        Print(indent..string.rep(" ",string.len(pos)+6).."}")
                    elseif (type(val)=="string") then
                        Print(indent.."["..pos..'] => "'..val..'"')
                    else
                        Print(indent.."["..pos.."] => "..tostring(val))
                    end
                end
            else
                Print(indent..tostring(t))
            end
        end
    end
    if (type(t)=="table") then
        Print(tostring(t).." {")
        sub_print_r(t,"  ")
        Print("}")
    else
        sub_print_r(t,"  ")
    end
    Print()
end


local last_index1, last_index2
local menu = Class(object)
sc_pr_menu = menu
function menu:init(exit_func)
    self.x = screen.width * 0.5 + screen.width
    self.y = screen.height * 0.5
    self.bound = false
    self.locked = true
    self.alpha = 1
    self.exit_func = exit_func
    self.index1 = 1
    self.index2 = 1
    self.authors = RecordAuthorList
    self.cards = {}
    self.texts = {}
    self.draws = {}
	self.allCardCount = { nonspell = 0, spell = 0 }
    if lstg.var.sc_pr and last_index1 and last_index2 then
        self.index1, self.index2 = last_index1, last_index2
        last_index1, last_index2 = nil, nil
        lstg.var.sc_pr = nil
    end
	menu.CalcAllCardCount(self)
    menu.UpdateList(self)
    menu.UpdateDraws(self)
end
function menu:frame()
    task.Do(self)
    if self.locked then
        return
    end
    menu.UpdateInput(self)
end
function menu:render()
    SetViewMode("ui")
    do
		SetImageState("white", "", Color(0xC0000000))
		RenderRect("white", self.x - 270, self.x - 150, self.y + 190, self.y - 190) --name bg
        for i = -7, 7 do
            local name = self.authors[(self.index1 + i - 1) % #self.authors + 1]
			local posdelta = i
            local alpha = 255 - (255-55) * abs(posdelta) / 7
            local x = self.x - 210
            local y = self.y + 25 * - posdelta
            if i==0 then
				renderRect(self.x - 270 - 15, self.x - 270,
							y - 10, y + 10, Color(255, 242, 136, 71))
				renderTTF("<", self.x - 270 - 7, y, 255, 153, 43, 2)
				renderRect(self.x - 270, self.x - 270 + 60,
							y - 10, y + 10,
							{Color(90, 242, 136, 71), Color(0, 242, 136, 71), Color(0, 242, 136, 71), Color(90, 242, 136, 71)})
				renderRect(self.x - 270 + 60, self.x - 150,
							y - 10, y + 10,
							{Color(0, 242, 136, 71), Color(90, 242, 136, 71), Color(90, 242, 136, 71), Color(0, 242, 136, 71)})
				renderRect(self.x - 150, self.x - 150 + 15,
							y - 10, y + 10, Color(255, 242, 136, 71))
				renderTTF(">", self.x - 150 + 7, y, 255, 153, 43, 2)
				renderTTF(name, x, y, alpha, 242, 136, 71)
			else
				renderTTF(name, x, y, alpha, 255, 255, 255)
			end
        end
		
		SetImageState("white", "", Color(0xC0000000))
		RenderRect("white", self.x - 270, self.x - 150, self.y + 215, self.y + 195) --nameCount bg
		renderTTF(string.format("%d / %d", self.index1, #self.authors), self.x - 210, self.y + 205, 255, 255, 255, 255)
    end
    do
		SetImageState("white", "", Color(0xC0000000))
		RenderRect("white", self.x - 125, self.x + 270, self.y + 190, self.y - 190) --spelllist bg
        menu.RenderSpellcardList(self, self.draws)
    end
end
function menu:RenderSpellcardList(texts)
	--实时计算结果
	local authorFullText = self.texts
	local counter = {totalscCount = 0, bossCardCount = {}}
	local bossIndex = 0
	for i=1,#authorFullText do
		local data = authorFullText[i]
		if data[2] then
			counter.totalscCount = counter.totalscCount + 1
			counter.bossCardCount[bossIndex] = counter.bossCardCount[bossIndex] + 1
		else
			bossIndex = bossIndex + 1
			counter.bossCardCount[bossIndex] = 0
		end
	end
	
	local baseY = self.y + 25 * 7
	local bossIndex = 0
    for i = 1, 15 do
        local data = texts[i]
        if data then
            if data[2] then
				local r, g, b = 255,255,255
				if data[4] == self.index2 then
					r, g, b = 242, 136, 71
					renderRect(self.x - 125, self.x + 270,
							baseY - 25 * (i - 1) - 10, baseY - 25 * (i - 1) + 10,
							{Color(0, 242, 136, 71), Color(90, 242, 136, 71), Color(90, 242, 136, 71), Color(0, 242, 136, 71)})
				end
                renderTTFR(data[5], self.x + 270 - 15, baseY - 25 * (i - 1), 255, r, g, b)
            else
				bossIndex = bossIndex + 1
                renderTTFL(data[3], self.x - 125 + 15, baseY - 25 * (i - 1), 255, 255, 255, 255)
                renderTTFR(string.format('(%d)', counter.bossCardCount[data[4]] or -1), self.x + 270 - 15, baseY - 25 * (i - 1), 255, 255, 255, 255)
            end
        else
            renderTTF("", self.x + 270 - 395/2, self.y - 25 * (i - 1), 255, 255, 255, 255)
        end
    end
	
	SetImageState("white", "", Color(0xC0000000))
	RenderRect("white", self.x - 125, self.x + 270, self.y + 215, self.y + 195) --spellCount bg
	renderTTFL(string.format("%d / %d", self.index2, counter.totalscCount), self.x - 125 + 15, self.y + 205, 255, 255, 255, 255)
	renderTTFR(string.format('ALL: %d (%d SC + %d NSC)', self.allCardCount.nonspell + self.allCardCount.spell, self.allCardCount.spell, self.allCardCount.nonspell), self.x + 270 - 15, self.y + 205, 255, 255, 255, 255)
	--renderTTFR('ALL: ???', self.x + 270 - 15, self.y + 205, 255, 255, 255, 255)
end
function menu:CalcAllCardCount()
    local a, b = 0, 0
    for _, author in ipairs(self.authors) do
        local _sorted_sc_table = RecordEditorDefinedClass[author]._sorted_sc_table
        for _, data in ipairs(_sorted_sc_table or {}) do
            for _, card in ipairs(data.card) do
                if card[4].is_sc then
                    b = b + 1
                else
                    a = a + 1
                end
            end
        end
    end
    self.allCardCount.nonspell = a
    self.allCardCount.spell = b
end
function menu:UpdateInput()
    local flag1, flag2 = false, false
    if MenuKeyIsPressed("left") then
        self.index1 = self.index1 - 1
        flag1 = true
    elseif MenuKeyIsPressed("right") then
        self.index1 = self.index1 + 1
        flag1 = true
    end
    self.index1 = (self.index1 - 1) % #self.authors + 1
    if MenuKeyIsPressed("up") then
        self.index2 = self.index2 - 1
        flag2 = true
    elseif MenuKeyIsPressed("down") then
        self.index2 = self.index2 + 1
        flag2 = true
    end
    self.index2 = (self.index2 - 1) % #self.cards + 1
    if flag1 or flag2 then
        PlaySound("select00", 0.3)
        if flag1 then
            menu.UpdateList(self)
            self.index2 = 1
        end
        menu.UpdateDraws(self)
    end
    if MenuKeyIsPressed "shoot" then
        local data = self.cards[self.index2]
        if data then
            PlaySound("ok00", 0.3)
            last_index1, last_index2 = self.index1, self.index2
            menu.SetCardData(self, data)
            if self.exit_func then
                self.exit_func(1)
            end
        else
            PlaySound("invalid", 0.5)
        end
    elseif MenuKeyIsPressed "spell" then
        PlaySound("cancel00", 0.3)
        menu.SetCardData(self, nil)
        if self.exit_func then
            self.exit_func(nil)
        end
    end
end
function menu:UpdateList()
    local cards = {}
    self.cards = cards
    local _sorted_sc_table = self.authors[self.index1] and RecordEditorDefinedClass[self.authors[self.index1]]._sorted_sc_table
    for _, data in ipairs(_sorted_sc_table or {}) do
        for _, card in ipairs(data.card) do
            insert(cards, { data.name, card[2], card[3], card[1], card[5], card[6] })
        end
    end
    local n = 0
    local texts = {}
    self.texts = texts
    do
        local boss_name
        local index = 0
		local bossIndex = 0
		texts.cardscount = {}
        for _, card in ipairs(self.cards) do
            n = n + 1
            if boss_name ~= card[2] then
				bossIndex = bossIndex + 1
                boss_name = card[2]
                insert(texts, { n, false, boss_name, bossIndex})
                n = n + 1
            end
            index = index + 1
            insert(texts, { n, true, boss_name, index, card[3] })
        end
    end
	--table.print(self.texts)
end
function menu:UpdateDraws()
    local draws = {}
    self.draws = draws
    local texts = self.texts
    local n = #texts
    if n <= 15 then
        for i = 1, n do
            insert(draws, texts[i])
        end
    else
		local lineIndexBossIndex = 0 --当前lineIndex对应的bossIndex
		local bossIndexDelta = 0 --需要倒推的index差数
        local lineIndex = nil
        for i = 1, n do
			if not texts[i][2] and not lineIndex then
				lineIndexBossIndex = lineIndexBossIndex + 1
			end
            if texts[i][2] and texts[i][4] == self.index2 then
                lineIndex = i
            end
        end
        if lineIndex <= 8 then
            for i = 1, 15 do
                insert(draws, texts[i])
            end
        else
            local remain = #texts - lineIndex
            if remain > 7 then
                for i = -7, 7 do
                    insert(draws, texts[lineIndex + i])
                end
				for i = lineIndex, max(1, lineIndex-7), -1 do
					if not texts[i][2] then bossIndexDelta = bossIndexDelta + 1 end
				end
            else
                for i = -14, 0 do
                    insert(draws, texts[#texts + i])
                end
				for i = lineIndex, #texts - 14, -1 do
					if not texts[i][2] then bossIndexDelta = bossIndexDelta + 1 end
				end
            end
            if draws[1][2] and not (draws[2][2]) then
                draws[1] = { draws[1][1], false, draws[1][3], lineIndexBossIndex-bossIndexDelta}
            elseif draws[1][2] and draws[2][2] then
                draws[1] = { draws[1][1], false, draws[2][3], lineIndexBossIndex-bossIndexDelta}
            end
        end
		--Print('lineIndexBossIndex', lineIndexBossIndex)
		--Print('bossIndexDelta', bossIndexDelta)
		--table.print(draws)
    end
end
function menu:SetCardData(data)
    if data then
        lstg.var.sc_pr = {
            class_name = data[4],
            index = data[5],
            perform = data[6],
        }
    else
        lstg.var.sc_pr = nil
    end
end

stage.group.DefStageFunc("Spell Practice@Spell Practice", "init", function(self)
    _init_item(self)
    New(mask_fader, "open")
    New(_G[lstg.var.player_name])
    task.New(self, function()
        if lstg.var.sc_pr then
            local boss_class = _editor_class[lstg.var.sc_pr.class_name]
            local card_index = lstg.var.sc_pr.index
            local cards = { boss_class.cards[card_index] }
            if lstg.var.sc_pr.perform then
                if boss_class.cards[card_index - 1] then
                    insert(cards, 1, boss_class.cards[card_index - 1])
                end
            else
                insert(cards, 1, boss.move.New(0, 144, 60, MOVE_DECEL))
            end
            local boss_bgm = boss_class.bgm
            if boss_bgm and boss_bgm:match("%S") then
                LoadMusicRecord(boss_bgm)
            end
            New(boss_class._bg or temple_background)
            task._Wait(30)
            if boss_bgm then
                local _, bgm = EnumRes("bgm")
                for _, v in pairs(bgm) do
                    local state = GetMusicState(v)
                    if v == boss_bgm then
                        if state == "paused" then
                            ResumeMusic(v)
                        elseif state == "stopped" then
                            PlayMusic(v)
                        end
                    else
                        StopMusic(v)
                    end
                end
            end
            local _ref = New(boss_class, cards)
            last = _ref
            while IsValid(_ref) do
                task.Wait()
            end
            task._Wait(150)
        end
        if ext.replay.IsReplay() then
            ext.pop_pause_menu = true
            ext.rep_over = true
            lstg.tmpvar.pause_menu_text = { "Replay Again", "Return to Title" }
        else
            ext.pop_pause_menu = true
            lstg.tmpvar.death = false
            lstg.tmpvar.pause_menu_text = { "Continue", "Quit and Save Replay", "Return to Title" }
        end
        task._Wait(60)
    end)
    task.New(self, function()
        while coroutine.status(self.task[1]) ~= "dead" do
            task.Wait()
        end
        New(mask_fader, "close")
        _stop_music()
        task.Wait(30)
        stage.group.FinishStage()
    end)
end)

Log("Inited in " .. (IsLuaSTGSub and ("LuaSTG Sub " .. lstg.GetVersionNumber()) or "LuaSTG Plus"))