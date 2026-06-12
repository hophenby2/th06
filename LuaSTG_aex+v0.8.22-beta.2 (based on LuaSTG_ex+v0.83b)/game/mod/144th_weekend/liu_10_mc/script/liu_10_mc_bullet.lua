local calc = require("liu_10_mc.script.liu_10_mc_math")
local func = calc.lerp
local rnd = calc.rnd
------------------------------------------------------------------
local lib = {}
------------------------------------------------------------------
local function LoadTexResouces()
    local dir = "liu_10_mc/img/bullet/"
    LoadTexture("liu_10_mc_etama", dir .. "liu_10_mc_etama.png")
    if not lstg.CheckRes(1, "liu_10_mc_etama2") then
        LoadTexture("liu_10_mc_etama2", dir .. "liu_10_mc_etama2.png")
    end
    LoadTexture("liu_10_mc_etama6", dir .. "liu_10_mc_etama6.png")
    LoadTexture("liu_10_mc_etama8", dir .. "liu_10_mc_etama8.png")
    LoadTexture("liu_10_mc_etama9", dir .. "liu_10_mc_etama9.png")
end
lib.LoadTexResouces = LoadTexResouces
------------------------------------------------------------------
local bulletGraphic = {}

--- @name,cols,rows,x,y,w,h,colli,tex,rect
local et_param = {
    [0] = {"ET_dot", 8, 2, 0, 240, 8, 8, 4, "liu_10_mc_etama", true},
    [1] = {"ET_dot2", 8, 2, 0, 240, 8, 8, 4, "liu_10_mc_etama", true},
    [2] = {"ET_mold", 8, 2, 0, 192, 8, 8, 4, "liu_10_mc_etama", true},
    [3] = {"ET_small", 16, 1, 0, 48, 16, 16, 6, "liu_10_mc_etama", true},
    [4] = {"ET_small2", 16, 1, 0, 48, 16, 16, 6, "liu_10_mc_etama", true},
    [5] = {"ET_ring", 16, 1, 0, 32, 16, 16, 6, "liu_10_mc_etama", true},
    [6] = {"ET_ring2", 16, 1, 0, 32, 16, 16, 6, "liu_10_mc_etama", true},
    [7] = {"ET_grain", 16, 1, 0, 65, 16, 14, 4, "liu_10_mc_etama", true},
    [8] = {"ET_kunai", 16, 1, 0, 81, 16, 14, 4, "liu_10_mc_etama", true},
    [9] = {"ET_needle", 16, 1, 0, 97, 16, 14, 4, "liu_10_mc_etama", true},
    [10] = {"ET_square", 16, 1, 1, 112, 14, 16, 4, "liu_10_mc_etama", true},
    [11] = {"ET_triangle", 16, 1, 1, 16, 14, 16, 4, "liu_10_mc_etama", true},
    [12] = {"ET_bullet", 16, 1, 1, 129, 14, 14, 4, "liu_10_mc_etama", true},
    [13] = {"ET_sb", 16, 1, 1, 177, 14, 14, 0, "liu_10_mc_etama", true},
    [14] = {"ET_long_mold", 16, 1, 1, 144, 14, 16, 4, "liu_10_mc_etama", true},
    [15] = {"ET_small_star", 16, 1, 1, 161, 14, 14, 6, "liu_10_mc_etama", true},
    [16] = {"ET_money", 3, 1, 208, 192, 16, 16, 6, "liu_10_mc_etama", true},
    [17] = {"ET_middle", 8, 1, 0, 32, 32, 32, 10, "liu_10_mc_etama6", true},
    [18] = {"ET_high_middle", 8, 1, 0, 32, 32, 32, 10, "liu_10_mc_etama6", true},
    [19] = {"ET_ellipse", 8, 1, 1, 129, 30, 30, 8, "liu_10_mc_etama6", true},
    [20] = {"ET_knife", 8, 1, 1, 97, 30, 30, 8, "liu_10_mc_etama6", true},
    [21] = {"ET_butterfly", 8, 1, 1, 65, 30, 30, 8, "liu_10_mc_etama6", true},
    [22] = {"ET_big_star", 8, 1, 1, 1, 30, 30, 8, "liu_10_mc_etama6", true},
    [23] = {"ET_water", 1, 1, 1, 177, 30, 30, 6, "liu_10_mc_etama2", true},
    [24] = {"ET_fire", 1, 1, 1, 145, 30, 30, 6, "liu_10_mc_etama2", true},
    [25] = {"ET_heart", 8, 1, 0, 0, 32, 32, 10, "liu_10_mc_etama8", true},
    [26] = {"ET_big", 4, 1, 0, 192, 64, 64, 14, "liu_10_mc_etama6", false},
    [27] = {"ET_rose", 4, 1, 0, 32, 64, 64, 14, "liu_10_mc_etama8", false},
    [28] = {"ET_drop", 16, 1, 0, 192, 16, 16, 4, "liu_10_mc_etama8", true},
    [29] = {"ET_purple_fire", 1, 1, 1, 209, 30, 30, 6, "liu_10_mc_etama8", true},
    [30] = {"ER_laser", 16, 1, 1, 1, 14, 14, 6, "liu_10_mc_etama", true},
}
------------------------------------------------------------------
for i, v in pairs(et_param) do
    bulletGraphic[i] = {}
    for j = 0, ((v[2] * v[3]) - 1) do
        bulletGraphic[i][j] = ("liu_10_mc_%s_%d"):format(v[1], j)
    end
    if (v[2] * v[3]) == 1 then
        bulletGraphic[i][0] = ("liu_10_mc_%s_0"):format(v[1], j)
    end
end

local bulletGroup = {
    color16 = {},
    color8 = {},
    color4 = {},
    color1 = {},
}

for i = 0, #bulletGraphic do
    local num = #bulletGraphic[i]
    if num == (16 - 1) then
        table.insert(bulletGroup.color16, i)
    elseif num == (8 - 1) then
        table.insert(bulletGroup.color8, i)
    elseif num == (4 - 1) then
        table.insert(bulletGroup.color4, i)
    elseif num == (1 - 1) then
        table.insert(bulletGroup.color1, i)
    end
end
------------------------------------------------------------------
local function LoadBulletResouces()
    for i = 0, #et_param do
        local tex = et_param[i][9]
        local rect = et_param[i][10]
        local m, n = et_param[i][2], et_param[i][3]
        local x, y, w, h = et_param[i][4], et_param[i][5], et_param[i][6], et_param[i][7]
        local a, b = et_param[i][8] / (rect and 2 or 1), et_param[i][8] / (rect and 2 or 1)
        local dx, dy = 0, 0
        if not(i == 23 or i == 24 or i == 29) then
            if (m == 8 and n == 2) then
                dx, dy = 8, 8
            elseif (m == 16 and n == 1) then
                dx, dy = 16, 0
            elseif (m == 3 and n == 1) then
                dx, dy = 16, 0
            elseif (m == 8 and n == 1) then
                dx, dy = 32, 0
            elseif (m == 4 and n == 1) then
                dx, dy = 64, 0
            end
            for j = 0, #bulletGraphic[i] do
                local name = bulletGraphic[i][j]
                LoadImage(name, tex, x + dx * (j % m), y + dy * int(j / m), w, h, a, b, rect)
            end
        else
            for j = 0, 3 do
                local name = bulletGraphic[i][0]:gsub("_0", "_" .. j)
                LoadImage(name, tex, x + 32 * j, y, w, h, a, b, rect)
            end
        end
    end
    --- 敌弹效果
    --- preimg
    for i = 0, 7 do
        LoadImage("liu_10_mc_preimg_" .. i, "liu_10_mc_etama", 1 + 32 * i, 209, 30, 30)
    end
    ---  etdel
    for i = 0, 15 do
        LoadImage("liu_10_mc_etdel_" .. i, "liu_10_mc_etama", 16 * i, 176, 16, 16)
    end
end
lib.LoadBulletResouces = LoadBulletResouces

local et_break = Class(object)
function et_break:init(x, y, index, layer)
    self.img = "liu_10_mc_etdel_" .. index
    self.layer = layer or LAYER_ENEMY_BULLET - 5
    self.group = GROUP_GHOST
    self.x, self.y = x, y
    self.pos = {rnd.Float(-1, 1) * 12, rnd.Float(-1, 1) * 12 + 24}
    self.rot = rnd.Float(-180, 180)
    self.scale = 1
    self.alpha = 128
    task.New(self, function()
        calc.LerpTo(self, "x", self.x + self.pos[1], 28, 0)
        calc.LerpTo(self, "y", self.y + self.pos[2], 28, 0)
        calc.LerpTo(self, "scale", 1.9, 14, 4)
        task.Wait(8)
        self.alpha = 20
        task.Wait(6)
        calc.LerpTo(self, "scale", 0.8, 14, 1)
        task.Wait(14)
        Del(self)
    end)
end
function et_break:frame()
    task.Do(self)
end
function et_break:render()
    local x, y = self.x, self.y
    local a = self.rot
    local co = Color(self.alpha, 255, 255, 255)
    local img = self.img
    local s = self.scale
    SetImageState(img, "mul+add", co)
    Render(img, x, y, a, s)
    SetImageState(img, "", Color(0xFFFFFFFF))
end

local function SetBulletPreimg(obj, mode, stay)
    mode = mode or 0
    local t = {8, 15, 25}
    local co, s1
    local s2 = 1
    local img
    local style = obj.style
    if style then
        if (style == 0 or style == 1 or style == 2) then
            s1, s2 = {2, 3, 4}, 0.5
            co = {0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7}
        elseif ((style >= 3 and style <= 16) or (style == 28 or style == 30)) then
            s1, s2 = {3, 3, 4}, 0.5
            co = {0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7}
            if style == 16 then co = {7, 8, 2} end
        elseif ((style >= 17 and style <= 25) or (style == 29)) then
            s1, s2 = {5, 5, 6}, 1
            co = {0, 1, 2, 3, 4, 5, 6, 7}
            if (style == 23 or style == 24 or style == 29) then
                img = bulletGraphic[style][0]
            end
        elseif (style == 26 or style == 27) then
            s1, s2 = {2, 3, 4}, 1
            img = obj.img
            co = {1, 3, 5, 6}
        end
    end
    obj.stay = stay or false
    obj.preimg = {}
    obj.preimg.frame = function(self)
        if not self.stay then
            if not(self._forbid_ref) then
                self._forbid_ref = true
                self.logclass.frame(self)
                self._forbid_ref = nil
            end
        else
            self.x = self.x - self.vx
            self.y = self.y - self.vy
            self.rot = self.rot - self.omiga
        end
        if self.timer == t[mode] then
            self.class = self.logclass
            if self.stay then
                self.timer = -1
            end
        end
        if self.rot ~= 0 then
            self.img_angle = self.rot
            self.rot = 0
        end
    end
    local blend = obj._blend or ""
    obj.preimg.render = function(self)
        if mode > 0 then
            local imgname = ""
            if img then
                imgname = img
            else
                imgname = "liu_10_mc_preimg_" .. co[(self._index % #co) + 1]
            end
            local rot = 0 + self.omiga * self.ani
            if self.move_rot then rot = self.rot end
            local s = func(s1[mode], s2, min(self.timer / t[mode], 1), 4)
            local al = func(0, 255, min(self.timer / t[mode], 1), 0)
            SetImageState(imgname, blend, Color(al, 255, 255, 255))
            Render(imgname, self.x, self.y, rot, s, s)
            SetImageState(imgname, "mul+alpha", Color(0xFFFFFFFF))
        end
    end
end
lib.SetBulletPreimg = SetBulletPreimg

local function BulletClassInit(obj, style, co)
    style = style or 0
    co = co or 0
    obj.style = (style % (#bulletGraphic + 1))
    obj._index = co % max((#bulletGraphic[style] + 1), 1)
    obj.img = bulletGraphic[style][co % max((#bulletGraphic[style] + 1), 1)]
    if ((style >= 0 and style <= 6) or (style >= 15 and style <= 18) or (style == 22 or style == 26 or style == 27)) then
        obj.move_rot = false
    else
        obj.move_rot = true
    end
    obj.layer = LAYER_ENEMY_BULLET - obj.style * 0.0001 - obj._index * 0.00001
end
lib.BulletClassInit = BulletClassInit

local function bulletImageChange(obj, style, co, preimg)
    style = style or 0
    co = co or 0
    obj.style = (style % (#bulletGraphic + 1))
    obj._index = co % max((#bulletGraphic[style] + 1), 1)
    if ((style >= 0 and style <= 6) or (style >= 15 and style <= 18) or (style == 22 or style == 26 or style == 27)) then
        obj.move_rot = false
    else
        obj.move_rot = true
    end
    obj.img = bulletGraphic[style][co % max((#bulletGraphic[style] + 1), 1)]
    if preimg then
        SetBulletPreimg(obj, preimg, false)
        obj.class = obj.imgclass
        obj.timer = -1
    end
end
lib.bulletImageChange = bulletImageChange

local tmp_class = Class(bullet)
function tmp_class:frame()
    task.Do(self)
    if (self.style == 23 or self.style == 24 or self.style == 29) then
        local t = int((self.timer / 3) % 4)
        self.img = bulletGraphic[self.style][0]:gsub("_0", "_" .. t)
    end
    if self.rot ~= 0 then
        self.img_angle = self.rot
        self.rot = 0
    end
end
function tmp_class:render()
    if self._blend and self._a and self._r and self._g and self._b then
        SetImageState(self.img, self._blend, Color(self._a, self._r, self._g, self._b))
    end
    local angle = self.img_angle or 0
    if self.move_rot then
        Render(self.img, self.x, self.y, angle - 90, self.hscale, self.vscale)
    else
        angle = 0 + self.ani * self.omiga
        Render(self.img, self.x, self.y, angle, self.hscale, self.vscale)
    end
    if self._blend and self._a and self._r and self._g and self._b then
        SetImageState(self.img, "", Color(0xFFFFFFFF))
    end
end
function tmp_class:del()
    if BoxCheck(self, lstg.world.boundl, lstg.world.boundr, lstg.world.boundb, lstg.world.boundt) then
        lib.bullet_class.del(self)
    end
end
function tmp_class:kill()
    if BoxCheck(self, lstg.world.boundl, lstg.world.boundr, lstg.world.boundb, lstg.world.boundt) then
        lib.bullet_class.kill(self)
    end
end

lib.bullet_class = Class(img_class)
lib.bullet_class.size = 1
function lib.bullet_class:init(index)
    self.logclass = tmp_class
end
function lib.bullet_class:frame()
    if self.preimg and self.preimg.frame then
        self.preimg.frame(self)
    else
        self.class = self.logclass
    end
end
function lib.bullet_class:render()
    if self.preimg and self.preimg.render then
        self.preimg.render(self)
    end
end
function lib.bullet_class:del()
    self.hscale, self.vscale = 1, 1
    self.class = self.logclass
    if self.style and self._index then
        if not self.delete then
            PreserveObject(self)
            self.delete = true
        end
        task.New(self, function()
            local m = 0
            local s1, s2 = 0.4, 1.9
            local t = 8
            local a1, a2 = 255, 0
            local style, co = self.style, self._index
            if (style == 15) then
                self._blend = ""
            else
                self._blend = "mul+add"
            end
            self._r, self._g, self._b = 255, 255, 255
            self.colli = false
            self.group = GROUP_GHOST
            if ((style >= 0 and style <= 16) or (style == 28 or style == 30)) then
                self.rot = rnd.Float(-180, 180)
                self.move_rot = true
                if style == 16 then
                    local c = {13, 15, 2}
                    self.img = "liu_10_mc_etdel_" .. c[max(co + 1, 1)]
                else
                    self.img = "liu_10_mc_etdel_" .. max(co + 1, 1)
                end
                New(et_break, self.x, self.y, co, self.layer + 1)
                if (style >= 0 and style <= 2) then
                    if (style == 2) then
                        s1, s2 = 0.8, 0
                        t = 16
                        a2 = 255
                    end
                else
                    s1, s2 = 1, 0
                    t = 16
                    a2 = 255
                end
            elseif ((style >= 17 and style <= 25) or (style == 29)) then
                local c = {0, 2, 4, 6, 8, 10, 13, 15}
                New(et_break, self.x, self.y, c[max(co + 1, 1)], self.layer + 1)
                s1, s2 = 1, 1.5
                t = 14
                a2 = 0
                if (style == 23 or style == 24 or style == 29) then
                    s1, s2 = 1.5, 2.9
                    t = 14
                    if (style == 23) then
                        self.img = "liu_10_mc_etdel_6"
                    elseif (style == 24) then
                        self.img = "liu_10_mc_etdel_2"
                    else
                        self.img = "liu_10_mc_etdel_4"
                    end
                end
            elseif (style == 26 or style == 27) then
                local c = {2, 4, 10, 13}
                New(et_break, self.x, self.y, c[max(co + 1, 1)], self.layer + 1)
                s1, s2 = 1, 0
                t = 12
                a2 = 0
            end
            if (style == 26 or style == 27) then m = 4 end
            SetV2(self, 0, 0, true, false)
            for i = 1, t do
                self.x = self.x
                self.y = self.y
                self._a = func(a1, a2, i / t, m)
                local s = func(s1, s2, i / t, 4)
                self.hscale = s
                self.vscale = s
                task.Wait(1)
            end
            RawDel(self)
        end)
    end
end
function lib.bullet_class:kill()
    New(item_faith_minor, self.x, self.y)
    lib.bullet_class.del(self)
end

local shotFunc = {
    [0] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            count = (way - 1) / 2
            for j = 1, way do
                local sa = (Angle(sx, sy, player) + ang1) + (count * ang2)
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = max(abs(count) - 1, 0)
                else
                    count = count * (-1)
                end
            end
        end
        return t
    end,
    [1] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            count = (way - 1) / 2
            for j = 1, way do
                local sa = ang1 + (count * ang2)
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = max(abs(count) - 1, 0)
                else
                    count = count * (-1)
                end
            end
        end
        return t
    end,
    [2] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            local da = ang2 * (i - 1)
            count = 0
            for j = 1, way do
                local sa = (Angle(sx, sy, player) + ang1 - da) + (count * (360 / way))
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = count * (-1)
                else
                    count = abs(count) + 1
                end
            end
        end
        return t
    end,
    [3] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            local da = ang2 * (i - 1)
            count = 0
            for j = 1, way do
                local sa = (ang1 - da) + (count * (360 / way))
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = count * (-1)
                else
                    count = abs(count) + 1
                end
            end
        end
        return t
    end,
    [4] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            local da = ang2 * (i - 1)
            count = 0
            for j = 1, way do
                local sa = (Angle(sx, sy, player) + ang1 + (180 / way) - da) + (count * (360 / way))
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = count * (-1)
                else
                    count = abs(count) + 1
                end
            end
        end
        return t
    end,
    [5] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            local da = ang2 * (i - 1)
            count = 0
            for j = 1, way do
                local sa = (ang1 + (180 / way) - da) + (count * (360 / way))
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = count * (-1)
                else
                    count = abs(count) + 1
                end
            end
        end
        return t
    end,
    [6] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            for j = 1, way do
                local sa = ran:Float(ang1 - ang2, ang1 + ang2)
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
            end
        end
        return t
    end,
    [7] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local da = ang2 * (i - 1)
            count = 0
            for j = 1, way do
                local sv = ran:Float(spd1, (spd1 + spd2))
                local sa = (ang1 - da) + (count * (360 / way))
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = count * (-1)
                else
                    count = abs(count) + 1
                end
            end
        end
        return t
    end,
    [8] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            for j = 1, way do
                local sv = ran:Float(spd1, (spd1 + spd2))
                local sa = ran:Float(ang1 - ang2, ang1 + ang2)
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
            end
        end
        return t
    end,
    [9] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            local da = ang2 * (i - 1)
            count = 0
            for j = 1, way do
                local et_num = 2
                if i == 1 then et_num = 1 end
                for k = 1, et_num do
                    if k == 2 then da = da * (-1) end
                    local sa = (Angle(sx, sy, player) + ang1 - da) + (count * (360 / way))
                    local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                    SetV2(et, sv, sa, true, false)
                    et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                    table.insert(t, et)
                end
                if ((j % 2) == 0) then
                    count = count * (-1)
                else
                    count = abs(count) + 1
                end
            end
        end
        return t
    end,
    [10] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            local da = ang2 * (i - 1)
            count = 0
            for j = 1, way do
                local et_num = 2
                if i == 1 then et_num = 1 end
                for k = 1, et_num do
                    if k == 2 then da = da * (-1) end
                    local sa = (ang1 - da) + (count * (360 / way))
                    local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                    SetV2(et, sv, sa, true, false)
                    et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                    table.insert(t, et)
                end
                if ((j % 2) == 0) then
                    count = count * (-1)
                else
                    count = abs(count) + 1
                end
            end
        end
        return t
    end,
    [11] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            count = 0
            for j = 1, way do
                local sa = ang1 + (count * (360 / way))
                local aa = abs(cos(sa - ang1))
                local vv = 0.75 * (aa ^ 2) + 0.25 * aa
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv + vv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = count * (-1)
                else
                    count = abs(count) + 1
                end
            end
        end
        return t
    end,
    [12] = function(num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
        param = param or {}
        local t = {}
        local count
        local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)
        for i = 1, layer do
            local sv = spd1 + ((spd2 - spd1) / layer) * (i - 1)
            count = (way - 1) / 2
            for j = 1, way do
                local sa = ang1 + (count * (360 / way))
                local aa = abs(cos(sa - ang1))
                local vv = 0.75 * (aa ^ 2) + 0.25 * aa
                local et = New(class, sx + dis * cos(sa), sy + dis * sin(sa), unpack(param))
                SetV2(et, sv + vv, sa, true, false)
                et.layer = et.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * num
                table.insert(t, et)
                if ((j % 2) == 0) then
                    count = max(abs(count) - 1, 0)
                else
                    count = count * (-1)
                end
            end
        end
        return t
    end,
}

lib.ShotBulletMode = function(style, num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
    return shotFunc[style](num, class, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)
end
------------------------------------------------------------------
--- laser

local GetLaser8Color = function(style)
    local co
    if (style == 0 or style == 1 or style == 2) then
        co = {0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7}
    elseif ((style >= 3 and style <= 16) or (style == 28 or style == 30)) then
        co = {0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7}
        if style == 16 then co = {7, 8, 2} end
    elseif ((style >= 17 and style <= 25) or (style == 29)) then
        co = {0, 1, 2, 3, 4, 5, 6, 7}
        if (style == 23) then
            co = 3
        elseif (style == 24) then
            co = 1
        elseif (style == 29) then
            co = 2
        end
    elseif (style == 26 or style == 27) then
        co = {1, 3, 5, 6}
    end
    return co
end

local LineLaser = plus.Class()
function LineLaser:init(obj, style, color, a, length, width, eff_co, destroy)
    self.obj = obj
    self.l, self.w = a, width
    self.max_l = length
    self.node = {}
    self.colli = true
    obj.colli = false
    obj.group = GROUP_INDES
    obj.layer = LAYER_ENEMY_BULLET - 5
    self.layer = obj.layer
    self.speed = 0
    self.angle = 0
    self.style = style
    self.co = color
    self.eff_co = eff_co or color
    self.pos = {obj.x, obj.y}
    self.head_t = 0
    self.pre_t = 0
    self.destroy = destroy or false
end
function LineLaser:frame()
    local obj = self.obj
    if not IsValid(obj) then return end
    self.speed = obj._speed
    self.angle = obj._angle
    local len = #self.node
    for i, v in ipairs(self.node) do
        if i == len then
            v.x, v.y = obj.x, obj.y
            break
        end
        local r = (self.l / len) * (len - i)
        v.x = obj.x + r * cos(self.angle)
        v.y = obj.y + r * sin(self.angle)
        v.a = self.angle
    end
    if self.l < self.max_l then
        if (obj.timer % 4) == 0 and self.speed > 0 then
            local list = {x = obj.x, y = obj.y, life = true, grazed = false}
            table.insert(self.node, list)
        end
        self.l = min(self.l + self.speed, self.max_l)
        obj.x, obj.y = unpack(self.pos)
    elseif self.l >= self.max_l then
        local killnum = 0
        for _, v in ipairs(self.node) do
            if not v.life then
                killnum = killnum + 1
            end
            if killnum >= (len - 1) then
                RawDel(obj)
            end
        end
    end
    if self.colli then
        local p = player
        for i, v in ipairs(self.node) do
            local L = 0
            if next(self.node, i) then
                L = Dist(v.x, v.y, self.node[i + 1].x, self.node[i + 1].y)
            else
                L = Dist(v.x, v.y, obj)
            end
            if i == len then break end
            if IsValid(p) and v.life and (p.death == 0 or p.death > 90) then
                local x, y = p.x - v.x, p.y - v.y
                x, y = calc.Rotate2D(x, y, self.angle)
                if x < L + p.a and x > 0 - p.a and y < (self.w * 0.75) / 2 + p.a and y > -(self.w * 0.75) / 2 - p.a then
                    if self.destroy then
                        v.life = false
                        if v.x >= -192 and v.x <= 192 and v.y >= -224 and v.y <= 224 then
                            New(et_break, v.x, v.y, self.eff_co, self.layer + 1)
                        end
                    end
                    if p.class.colli then p.class.colli(p, obj) end
                end
                if p.grazer and IsValid(p.grazer) and v.grazed == false then
                    if x < L + p.grazer.a and x > 0 - p.grazer.a and y < (self.w * 0.75) / 2 + p.grazer.a and y > -(self.w * 0.75) / 2 - p.grazer.a then
                        item.PlayerGraze()
                        p.grazer.grazed = true
                        v.grazed = true
                    end
                end
            end
        end
    end
    self.head_t = self.head_t + 1
    if self.head_t > 9 then self.head_t = 5 end
    self.pre_t = self.pre_t + 1
end
function LineLaser:render()
    local obj = self.obj
    if not IsValid(obj) then return end
    local rendernode = {}
    local lasttail = 0
    local len = #self.node
    for i, v in ipairs(self.node) do
        local n, m = 0, i
        if v.life and i >= lasttail then
            for j = i, len do
                if self.node[j].life then
                    n, m = j, i
                else
                    lasttail = min(j + 1, #self.node)
                    break
                end
            end
            table.insert(rendernode, {n, m})
        end
        if n >= len then break end
    end
    for _, v in ipairs(rendernode) do
        local n, m = unpack(v)
        local x, y = self.node[m].x, self.node[m].y
        local L = 0
        if n == #self.node then
            L = Dist(x, y, obj)
        else
            L = Dist(x, y, self.node[n].x, self.node[n].y)
        end
        local a = self.angle
        local w = self.w / 2
        local blend = "mul+add"
        local c = Color(0xFFFFFFFF)
        if obj._blend and obj._a and obj._r and obj._g and obj._b then
            blend, c = obj._blend, Color(obj._a, obj._r, obj._g, obj._b)
        end
        local img = bulletGraphic[self.style][self.co]
        SetImageState(img, blend, c)
        Render4V(img,
            x + w * cos(a - 90), y + w * sin(a - 90), 0.5,
            x + w * cos(a + 90), y + w * sin(a + 90), 0.5,
            x + w * cos(a + 90) - L * cos(a), y + w * sin(a + 90) - L * sin(a), 0.5,
            x + w * cos(a - 90) - L * cos(a), y + w * sin(a - 90) - L * sin(a), 0.5)
        SetImageState(img, "", Color(0xFFFFFFFF))
        local co = GetLaser8Color(self.style)
        img = "liu_10_mc_laserHead_"
        if type(co) == "table" then
            img = img .. co[self.co]
        elseif type(co) == "number" then
            img = img .. co
        end
        local t = self.head_t
        if t >= 5 then
            local s, al = 1, 255
            if t > 5 and t <= 7 then
                local tt = t - 5
                s = func(1, 0.8, min(tt / 2, 1), 0)
                al = func(128, 255, min(tt / 2, 1), 0)
            elseif t > 7 and t <= 9 then
                local tt = t - 7
                s = func(0.8, 1, min(tt / 2, 1), 0)
                al = func(255, 128, min(tt / 2, 1), 0)
            end
            SetImageState(img, "mul+add", Color(al, 255, 255, 255))
            Render(img, x, y, 0, s)
            SetImageState(img, "", Color(0xFFFFFFFF))
        end
    end
    if self.l < self.max_l then
        local x, y = obj.x, obj.y
        local rot = -22.5 * self.pre_t
        local s = 3
        local al = func(0, 255, min(self.pre_t / 8, 1), 0)
        local co = GetLaser8Color(self.style)
        local img = "liu_10_mc_preimg_"
        if type(co) == "table" then
            img = img .. co[self.co]
        elseif type(co) == "number" then
            img = img .. co
        end
        if (self.pre_t % 2) == 0 then
            s = 1.5
        else
            s = 1.2
        end
        SetImageState(img, "mul+add", Color(al, 255, 255, 255))
        Render(img, x, y, rot, s * (self.w / 30))
        SetImageState(img, "", Color(0xFFFFFFFF))
    end
end
function LineLaser:del()
    local obj = self.obj
    if not IsValid(obj) then return end
    for _, v in ipairs(self.node) do
        if v.life then
            v.life = false
            if v.x >= -192 and v.x <= 192 and v.y >= -224 and v.y <= 224 then
                New(et_break, v.x, v.y, self.eff_co, self.layer + 1)
            end
        end
    end
end
function LineLaser:kill()
    local obj = self.obj
    if not IsValid(obj) then return end
    for _, v in ipairs(self.node) do
        if v.life then
            v.life = false
            New(item_faith_minor, v.x, v.y)
            if v.x >= -192 and v.x <= 192 and v.y >= -224 and v.y <= 224 then
                New(et_break, v.x, v.y, self.eff_co, self.layer + 1)
            end
        end
    end
end
------------------------------------------------------------------
local InfLaser = plus.Class()
function InfLaser:init(obj, style, color, a, length, b, width, t1, t2, t3, t4, eff_co, destroy)
    self.obj = obj
    self.l, self.w = a, b
    self.max_l, self.max_w = length, width
    self.node = {}
    self.colli = false
    obj.colli = false
    obj.group = GROUP_INDES
    obj.layer = LAYER_ENEMY_BULLET - 5
    self.layer = obj.layer
    self.speed = 0
    self.angle = 0
    self.style = style
    self.co = color
    self.eff_co = eff_co or color
    self.pos = {obj.x, obj.y}
    self.head_t = 0
    self.pre_t = 0
    self.t = {t1, t2, t3, t4}
    self.destroy = destroy or false
end
function InfLaser:frame()
    local obj = self.obj
    if not IsValid(obj) then return end
    self.speed = obj._speed
    self.angle = obj._angle
    if self.l < self.max_l then
        if (obj.timer % 4) == 0 and self.speed > 0 then
            local list = {x = obj.x, y = obj.y, life = true, a = (self.angle or 0), l = 0}
            table.insert(self.node, list)
        end
    end
    local len = #self.node
    local k = 0
    for i = len, 1, -1 do
        if self.node[i] and not(self.node[i].life) and not(self.delete) then
            k = i
            break
        elseif self.node[i] and self.node[i].life and not(self.delete) then
            if self.l < self.max_l then
                self.node[i].l = min(self.node[i].l + self.speed, self.max_l)
            end
        end
        self.node[i].x = obj.x + self.node[i].l * cos(self.node[i].a)
        self.node[i].y = obj.y + self.node[i].l * sin(self.node[i].a)
        self.node[i].a = self.angle
    end
    if k > 0 then
        local node = self.node[min(k + 1, len)]
        self.l = Dist(obj.x, obj.y, node.x, node.y)
    else
        self.l = min(self.l + self.speed, self.max_l)
    end
    for i = k, 1, -1 do
        if self.node[i].l < self.max_l then
            self.node[i].l = min(self.node[i].l + self.speed, self.max_l)
        end
        self.node[i].x = obj.x + self.node[i].l * cos(self.node[i].a)
        self.node[i].y = obj.y + self.node[i].l * sin(self.node[i].a)
        self.node[i].a = self.angle
        if self.node[k] and self.node[i] and  self.node[k].l >= self.max_l and not(self.delete) then
            table.remove(self.node, i)
        end
    end
    if self.delete then
        local w = lstg.world
        if BoxCheck(obj, w.boundl, w.boundr, w.boundb, w.boundt) then
            RawDel(obj)
        end
    else
        obj.x, obj.y = unpack(self.pos)
    end
    if self.colli then
        local p = player
        for i, v in ipairs(self.node) do
            local L = 0
            if next(self.node, i) then
                L = Dist(v.x, v.y, self.node[i + 1].x, self.node[i + 1].y)
            else
                L = Dist(v.x, v.y, obj)
            end
            if i == len then break end
            if IsValid(p) and v.life and (p.death == 0 or p.death > 90) then
                local x, y = p.x - v.x, p.y - v.y
                x, y = calc.Rotate2D(x, y, self.angle)
                if x < L + p.a and x > 0 - p.a and y < (self.w * 0.75) / 2 + p.a and y > -(self.w * 0.75) / 2 - p.a then
                    if self.destroy then
                        v.life = false
                        if v.x >= -192 and v.x <= 192 and v.y >= -224 and v.y <= 224 then
                            New(et_break, v.x, v.y, self.eff_co, self.layer + 1)
                        end
                    end
                    if p.class.colli then p.class.colli(p, obj) end
                end
                if p.grazer and IsValid(p.grazer) and self.grazed == false and (obj.timer % 5) == 0 then
                    if x < L + p.grazer.a and x > 0 - p.grazer.a and y < (self.w * 0.75) / 2 + p.grazer.a and y > -(self.w * 0.75) / 2 - p.grazer.a then
                        item.PlayerGraze()
                        p.grazer.grazed = true
                        self.grazed = true
                    end
                end
            end
        end
        if (obj.timer % 5) ~= 0 then
            self.grazed = false
        end
    end
    local t1, t2, t3, t4 = unpack(self.t)
    local t = obj.timer
    if t >= 0 and t < t1 then
        self.w = 1
    elseif t >= t1 and t < (t1 + t2) then
        local tt = t - t1
        self.w = (self.max_w - 1) * min(tt / t2, 1)
    elseif t >= (t1 + t2) and t < (t1 + t2 + t3) then
        self.colli = true
        self.w = self.max_w
    elseif t >= (t1 + t2 + t3) and t < (t1 + t2 + t3 + t4) then
        self.colli = false
        local tt = t - (t1 + t2 + t3)
        self.w = self.max_w * (1 - min(tt / t4, 1))
    elseif t >= (t1 + t2 + t3 + t4) then
        self.w = 0
        RawDel(obj)
    end
    self.pre_t = self.pre_t + 1
end
function InfLaser:render()
    local obj = self.obj
    if not IsValid(obj) then return end
    local rendernode = {}
    local lasttail = 0
    local len = #self.node
    for i, v in ipairs(self.node) do
        local n, m = 0, i
        if v.life and i >= lasttail then
            for j = i, len do
                if self.node[j].life then
                    n, m = j, i
                else
                    lasttail = min(j + 1, #self.node)
                    break
                end
            end
            table.insert(rendernode, {n, m})
        end
        if n >= len then break end
    end
    for _, v in ipairs(rendernode) do
        local n, m = unpack(v)
        local x, y = self.node[m].x, self.node[m].y
        local L = 0
        if n == #self.node then
            L = Dist(x, y, obj)
        else
            L = Dist(x, y, self.node[n].x, self.node[n].y)
        end
        local a = self.angle
        local w = self.w / 2
        local blend = "mul+add"
        local c = Color(0xFFFFFFFF)
        if obj._blend and obj._a and obj._r and obj._g and obj._b then
            blend, c = obj._blend, Color(obj._a, obj._r, obj._g, obj._b)
        end
        local img = bulletGraphic[self.style][self.co]
        SetImageState(img, blend, c)
        Render4V(img,
            x + w * cos(a - 90), y + w * sin(a - 90), 0.5,
            x + w * cos(a + 90), y + w * sin(a + 90), 0.5,
            x + w * cos(a + 90) - L * cos(a), y + w * sin(a + 90) - L * sin(a), 0.5,
            x + w * cos(a - 90) - L * cos(a), y + w * sin(a - 90) - L * sin(a), 0.5)
        SetImageState(img, "", Color(0xFFFFFFFF))
    end
    if not(self.delete) then
        local x, y = obj.x, obj.y
        local rot = -22.5 * self.pre_t
        local s = 3
        local al = func(0, 255, min(self.pre_t / 8, 1), 0)
        local co = GetLaser8Color(self.style)
        local img = "liu_10_mc_preimg_"
        if type(co) == "table" then
            img = img .. co[self.co]
        elseif type(co) == "number" then
            img = img .. co
        end
        if (self.pre_t % 2) == 0 then
            s = 1.5
        else
            s = 1.2
        end
        SetImageState(img, "mul+add", Color(al, 255, 255, 255))
        Render(img, x, y, rot, s * (self.max_w / 30))
        SetImageState(img, "", Color(0xFFFFFFFF))
    end
end
function InfLaser:del()
    if not(self.delete) and IsValid(self.obj) then
        PreserveObject(self.obj)
        self.delete = true
    end
end
function InfLaser:kill()
    local obj = self.obj
    if not IsValid(obj) then return end
    for _, v in ipairs(self.node) do
        if v.life then
            v.life = false
            New(item_faith_minor, v.x, v.y)
            if v.x >= -192 and v.x <= 192 and v.y >= -224 and v.y <= 224 then
                New(et_break, v.x, v.y, self.eff_co, self.layer + 1)
            end
        end
    end
end
------------------------------------------------------------------
local CurvedLaser = plus.Class()
function CurvedLaser:init(obj, color, length, width, eff_co, destroy)
    self.obj = obj
    self.l, self.w = length, width
    self.node = {}
    self.colli = true
    obj.colli = false
    obj.group = GROUP_INDES
    obj.layer = LAYER_ENEMY_BULLET - 5
    self.layer = obj.layer
    self.bound = obj.bound
    obj.bound = false
    self.speed = 0
    self.angle = 0
    self.co = color
    self.eff_co = eff_co or color
    self.pos = {obj.x, obj.y}
    self.pre_t = 0
    self.destroy = destroy or false
    self.data = {}
end
function CurvedLaser:frame()
    local obj = self.obj
    if not IsValid(obj) then return end
    self.speed = obj._speed
    self.angle = obj._angle
    if #self.node < self.l then
        local list = {x = self.pos[1], y = self.pos[2], dx = 0, dy = 0, a = (self.angle or 0), life = true, grazed = false}
        table.insert(self.node, list)
    end
    for i = #self.node, 1, -1 do
        local v = self.node[i]
        local tmp_pos = {v.x, v.y}
        if i == 1 then
            v.x, v.y = obj.x, obj.y
            v.dx, v.dy = v.x - tmp_pos[1], v.y - tmp_pos[2]
        else
            v.x, v.y = self.node[i - 1].x, self.node[i - 1].y
            v.dx, v.dy = v.x - tmp_pos[1], v.y - tmp_pos[2]
        end
        self.node[i].a = atan2(v.dy, v.dx)
    end
    for i, v in ipairs(self.node) do
        if i == self.l then break end
        if next(self.node, i) then
            local n = self.node[i + 1]
            local len = Dist(v.x, v.y, n.x, n.y)
            v.dis = len
        end
    end
    local len = #self.node - 1
    if self.colli then
        local p = player
        local w = self.w
        for i, v in ipairs(self.node) do
            if i > len then break end
            if IsValid(p) and v.life then
                local L = v.dis
                local x, y = v.x - (L / 2) * cos(v.a), v.y - (L / 2) * sin(v.a)
                if (Dist(x, y, p) ^ 2) < (p.a ^ 2 + ((w * 0.5) / 2) ^ 2) then
                    if self.destroy then
                        for j = i, 1, -1 do
                            if self.node[j].life then
                                self.node[j].life = false
                                local k = self.node[j]
                                if (j % 4) == 0 then
                                    if k.x >= -192 and k.x <= 192 and k.y >= -224 and k.y <= 224 then
                                        New(et_break, k.x, k.y, self.eff_co, self.layer + 1)
                                    end
                                end
                            end
                        end
                    end
                    if p.class.colli then p.class.colli(p, obj) end
                end
                if ((Dist(x, y, p) ^ 2) < ((max(40, ((w * 0.5) / 2) / 2.5) + p.a) ^ 2) + (((w * 0.5) / 2) ^ 2)) and v.grazed == false then
                    item.PlayerGraze()
                    if p.grazer and IsValid(p.grazer) then
                        p.grazer.grazed = true
                    end
                    v.grazed = true
                end
            end
        end
    end
    local count = 0
    for i, v in ipairs(self.node) do
        local w = lstg.world
        if self.bound and (v.x < w.boundl or v.x > w.boundr or v.y < w.boundb or v.y > w.boundt) then
            count = count + 1
        end
    end
    if count == #self.node then RawDel(obj) end
    len = #self.node
    if len == self.l then
        local killnum = 0
        for _, v in ipairs(self.node) do
            if not(v.life) then
                killnum = killnum + 1
            end
        end
        if killnum == (len - 1) then
            RawDel(obj)
        end
    end
    self.pre_t = self.pre_t + 1
    local lasttail = 0
    len = #self.node
    local list = {}
    for i, v in ipairs(self.node) do
        local n = 0
        if v.life and i >= lasttail then
            local tmp = {}
            for j = i, len do
                if self.node[j].life then
                    n =  j
                    table.insert(tmp, j)
                else
                    lasttail = min(j + 1, #self.node)
                    break
                end
            end
            table.insert(list, tmp)
        end
        if n >= len then break end
    end
    for i, v in ipairs(self.data) do
        v:Release()
        self.data[i] = nil
    end
    self.data = {}
    for i, v in ipairs(list) do
        self.data[i] = BentLaserData()
        local node = self.node
        local x, y = {}, {}
        for j, k in ipairs(v) do
            x[j], y[j] = node[k].x, node[k].y
        end
        self.data[i]:UpdateAllNode(#v, x, y, self.w)
    end
end
function CurvedLaser:render()
    local obj = self.obj
    if not IsValid(obj) then return end
    for i, v in ipairs(self.data) do
        local co = Color(0xFFFFFFFF)
        local blend = "mul+add"
        local w = self.w / 2
        if obj._blend and obj._a and obj._r and obj._g and obj._b then
            blend = obj._blend
            co = Color(obj._a, obj._r, obj._g, obj._b)
        end
        local tex = "liu_10_mc_etama9"
        local tx, ty, tw, th = 0, self.co * 16, 256, 16
        v:Render(tex, blend, co, tx, ty, tw, th)
    end
    if #self.node < self.l then
        local rot = -22.5 * self.pre_t
        local s = 3
        local al = func(0, 255, min(self.pre_t / 8, 1), 0)
        local co = {0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7}
        local img = "liu_10_mc_preimg_"
        if type(co) == "table" then
            img = img .. co[self.co]
        elseif type(co) == "number" then
            img = img .. co
        end
        if (self.pre_t % 2) == 0 then
            s = 1.5
        else
            s = 1.2
        end
        SetImageState(img, "mul+add", Color(al, 255, 255, 255))
        Render(img, self.pos[1], self.pos[2], rot, s * (self.w / 30))
        SetImageState(img, "", Color(0xFFFFFFFF))
    end
end
function CurvedLaser:del()
    local obj = self.obj
    obj.bound = true
    if not IsValid(obj) then return end
    for i, v in ipairs(self.node) do
        if v.life and i % 4 == 0 then
            v.life = false
            if v.x >= -192 and v.x <= 192 and v.y >= -224 and v.y <= 224 then
                New(et_break, v.x, v.y, self.eff_co, self.layer + 1)
            end
        end
    end
end
function CurvedLaser:kill()
    local obj = self.obj
    obj.bound = true
    if not IsValid(obj) then return end
    for i, v in ipairs(self.node) do
        if v.life and i % 4 == 0 then
            v.life = false
            New(item_faith_minor, v.x, v.y)
            if v.x >= -192 and v.x <= 192 and v.y >= -224 and v.y <= 224 then
                New(et_break, v.x, v.y, self.eff_co, self.layer + 1)
            end
        end
    end
end
------------------------------------------------------------------
lib.Laser = function(obj, style, color, a, length, b, width, t1, t2, t3, t4, eff_co, destroy)
    if t1 == 0 and t2 == 0 and t3 == 0 and t4 == 0 then
        return LineLaser(obj, style, color, a, length, width, eff_co, destroy)
    elseif t1 == -1 and t2 == -1 and t3 == -1 and t4 == -1 then
        return CurvedLaser(obj, color, length, width, eff_co, destroy)
    elseif t1 > 0 or t2 > 0 or t3 > 0 or t4 > 0 then
        return InfLaser(obj, style, color, a, length, b, width, t1, t2, t3, t4, eff_co, destroy)
    end
end
------------------------------------------------------------------
return lib