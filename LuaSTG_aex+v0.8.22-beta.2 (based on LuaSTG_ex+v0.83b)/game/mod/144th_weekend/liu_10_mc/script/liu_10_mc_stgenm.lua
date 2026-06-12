local calc = require("liu_10_mc.script.liu_10_mc_math")
local func = calc.lerp
local wisys = require("liu_10_mc.script.liu_10_mc_WalkImageSys")
local cdbg = require("liu_10_mc.script.liu_10_mc_cdbg")
local draw = require("liu_10_mc.script.liu_10_mc_draw")
------------------------------------------------------------
local lib = {}
------------------------------------------------------------
local LoadTexResouces = function()
    local dir = "liu_10_mc/img/stgenm/"
    LoadTexture("liu_10_mc_stage05e02", dir .. "liu_10_mc_stage05e02.png")
    SetTextureSamplerState("liu_10_mc_stage05e02", "linear+wrap")
    LoadTexture("liu_10_mc_stage06e01", dir .. "liu_10_mc_stage06e01.png")
    SetTextureSamplerState("liu_10_mc_stage06e01", "linear+wrap")
    LoadTexture("liu_10_mc_stage06e02", dir .. "liu_10_mc_stage06e02.png")
    SetTextureSamplerState("liu_10_mc_stage06e02", "linear+wrap")
    LoadTexture("liu_10_mc_stage06e03", dir .. "liu_10_mc_stage06e03.png")
    SetTextureSamplerState("liu_10_mc_stage06e03", "linear+wrap")
    dir = "liu_10_mc/img/card/"
    LoadTexture("liu_10_mc_cdbg06a", dir .. "liu_10_mc_cdbg06a.png")
    SetTextureSamplerState("liu_10_mc_cdbg06a", "linear+wrap")
    LoadTexture("liu_10_mc_cdbg06b", dir .. "liu_10_mc_cdbg06b.png")
    SetTextureSamplerState("liu_10_mc_cdbg06b", "linear+wrap")
end
lib.LoadTexResouces = LoadTexResouces
------------------------------------------------------------
local sprites = {
    ["stage06e01"] = {
        tex = "liu_10_mc_stage06e01",
        [0] = {x = 0, y = 0, w = 96, h = 128},
        [1] = {x = 96, y = 0, w = 96, h = 128},
        [2] = {x = 192, y = 0, w = 96, h = 128},
        [3] = {x = 288, y = 0, w = 96, h = 128},
        [4] = {x = 0, y = 128, w = 96, h = 128},
        [5] = {x = 96, y = 128, w = 96, h = 128},
        [6] = {x = 192, y = 128, w = 96, h = 128},
        [7] = {x = 288, y = 128, w = 96, h = 128},
        [8] = {x = 0, y = 256, w = 96, h = 128},
        [9] = {x = 96, y = 256, w = 96, h = 128},
        [10] = {x = 192, y = 256, w = 96, h = 128},
        [11] = {x = 288, y = 256, w = 96, h = 128},
        [12] = {x = 1, y = 385, w = 94, h = 126},
        [13] = {x = 97, y = 385, w = 94, h = 126},
        [14] = {x = 193, y = 385, w = 94, h = 126},
        [15] = {x = 289, y = 385, w = 94, h = 126},
    },
    ["cdbg06a"] = {
        tex = "liu_10_mc_cdbg06a",
        [0] = {x = 0, y = 0, w = 256, h = 256},
    },
    ["cdbg06b"] = {
        tex = "liu_10_mc_cdbg06b",
        [0] = {x = 0, y = 0, w = 512, h = 512},
    },
    ["stage06e02"] = {
        tex = "liu_10_mc_stage06e02",
        [0] = {x = 0, y = 0, w = 384, h = 224},
        [1] = {x = 384, y = 0, w = 80, h = 80},
        [2] = {x = 384, y = 80, w = 80, h = 80},
        [3] = {x = 384, y = 160, w = 32, h = 32},
    },
    ["stage06e03"] = {
        tex = "liu_10_mc_stage06e03",
        [0] = {x = 0, y = 0, w = 256, h = 256},
    },
    ["stage05e02"] = {
        tex = "liu_10_mc_stage05e02",
        [0] = {x = 0, y = 128, w = 122, h = 128},
        [1] = {x = 128, y = 128, w = 122, h = 128},
        [2] = {x = 0, y = 0, w = 512, h = 32},
        [3] = {x = 0, y = 32, w = 64, h = 64},
    }
}
------------------------------------------------------------
local walkimage = {
    {
        sprite = sprites["stage06e01"],
        {0, sprites["stage06e01"][0]},
        {12, sprites["stage06e01"][1]},
        {24, sprites["stage06e01"][2]},
        {36, sprites["stage06e01"][3]},
        {48, sprites["stage06e01"][0]},
        {60, sprites["stage06e01"][1]},
        {72, sprites["stage06e01"][2]},
        {84, sprites["stage06e01"][3]},
    },
    {
        sprite = sprites["stage06e01"],
        {0, sprites["stage06e01"][8]},
        {6, sprites["stage06e01"][9]},
        {12, sprites["stage06e01"][10]},
        {18, sprites["stage06e01"][11]},
    },
    {
        sprite = sprites["stage06e01"],
        {0, sprites["stage06e01"][4]},
        {6, sprites["stage06e01"][5]},
        {12, sprites["stage06e01"][6]},
        {18, sprites["stage06e01"][7]},
    },
    {
        sprite = sprites["stage06e01"],
        {0, sprites["stage06e01"][11]},
        {6, sprites["stage06e01"][10]},
        {12, sprites["stage06e01"][9]},
        {18, sprites["stage06e01"][0]},
        {30, sprites["stage06e01"][1]},
        {42, sprites["stage06e01"][2]},
        {54, sprites["stage06e01"][3]},
        {66, sprites["stage06e01"][0]},
        {78, sprites["stage06e01"][1]},
        {90, sprites["stage06e01"][2]},
        {102, sprites["stage06e01"][3]},
    },
    {
        sprite = sprites["stage06e01"],
        {0, sprites["stage06e01"][7]},
        {6, sprites["stage06e01"][6]},
        {12, sprites["stage06e01"][5]},
        {18, sprites["stage06e01"][0]},
        {30, sprites["stage06e01"][1]},
        {42, sprites["stage06e01"][2]},
        {54, sprites["stage06e01"][3]},
        {66, sprites["stage06e01"][0]},
        {78, sprites["stage06e01"][1]},
        {90, sprites["stage06e01"][2]},
        {102, sprites["stage06e01"][3]},
    },
    {
        sprite = sprites["stage06e01"],
        {0, sprites["stage06e01"][12]},
        {5, sprites["stage06e01"][13]},
        {10, sprites["stage06e01"][14]},
        {15, sprites["stage06e01"][15]},
    },
}
------------------------------------------------------------
local function SetWalkImage(self, list, id, t, hs, vs, rot, omiga)
    local p = list[id]
    self.tex = p.sprite.tex
    for _, v in ipairs(p) do
        if t == v[1] then
            local walk = self.sprite
            walk.x, walk.y, walk.w, walk.h = v[2].x, v[2].y, v[2].w, v[2].h
        end
    end
    self.hs, self.vs = hs or 1, vs or 1
    if rot then
        self.rot, self.tmp_rot = rot, self.rot
    end
    if omiga then
        self.omiga = omiga
    end
end
------------------------------------------------------------
local walkfunc = {
    function(self, obj)
        local t = self.count
        SetWalkImage(self, walkimage, 1, t, 1)
        local sys = obj._wisys
        if t >= 0 and t < 48 then
            local tt = t
            wisys.PosTime(sys, tt, 48, 9, 0, 4)
        elseif t >= 48 and t < 96 then
            local tt = t - 48
            wisys.PosTime(sys, tt, 48, 9, 0, -4)
        elseif t >= 96 then
            self.count = -1
        end
    end,
    function(self, obj)
        local t = self.count
        SetWalkImage(self, walkimage, 2, t, 1)
    end,
    function(self, obj)
        local t = self.count
        SetWalkImage(self, walkimage, 3, t, 1)
    end,
    function(self, obj)
        local t = self.count
        SetWalkImage(self, walkimage, 4, t, 1)
        local sys = obj._wisys
        if t >= 18 and t < 66 then
            local tt = t - 18
            wisys.PosTime(sys, tt, 48, 9, 0, 4)
        elseif t >= 66 and t < 114 then
            local tt = t - 66
            wisys.PosTime(sys, tt, 48, 9, 0, -4)
        elseif t >= 114 then
            self.count = 17
        end
    end,
    function(self, obj)
        local t = self.count
        SetWalkImage(self, walkimage, 5, t, 1)
        local sys = obj._wisys
        if t >= 18 and t < 66 then
            local tt = t - 18
            wisys.PosTime(sys, tt, 48, 9, 0, 4)
        elseif t >= 66 and t < 114 then
            local tt = t - 66
            wisys.PosTime(sys, tt, 48, 9, 0, -4)
        elseif t >= 114 then
            self.count = 17
        end
    end,
    function(self, obj)
        local t = self.count
        SetWalkImage(self, walkimage, 6, t, 1)
        if t >= 20 then
            self.count = 9
        end
    end,
    function(self, obj)
        local t = self.count
        SetWalkImage(self, walkimage, 6, t, -1)
        if t >= 20 then
            self.count = 9
        end
    end,
}
------------------------------------------------------------
lib.SetBossWalkImage = function(obj)
    local state = {}
    for i = 1, #walkfunc do
        state[i] = ("%d"):format(i)
    end
    obj._wisys = wisys.wisys(obj, walkfunc, state, 1)
end
------------------------------------------------------------
lib.cardbg =  Class(_spellcard_background)
local cardbg = lib.cardbg
function cardbg:init()
    _spellcard_background.init(self)
    local sprite = sprites["cdbg06a"]
    self.layer = LAYER_BG + 1
    cdbg.AddLayer(self, sprite.tex, {sprite[0].x, sprite[0].y, sprite[0].w, sprite[0].h},
    0, 0, 0, 0.00125, 0, 0, "", {1.5, 1.75}, cdbg.defaultFrame, {0, 0}, Color(255, 255, 255, 255))
    sprite = sprites["cdbg06b"]
    cdbg.AddLayer(self, sprite.tex, {sprite[0].x, sprite[0].y, sprite[0].w, sprite[0].h},
    0, 0, 0, 0, 0, -0.3, "", {1, 1}, cdbg.defaultFrame, {0, 0}, Color(255, 255, 255, 255))
end
function cardbg:render()
    cdbg.renderFunc(self)
end
------------------------------------------------------------
local ShadowR = Class(object)
function ShadowR:init(x, y)
    self.tex = sprites["stage06e01"].tex
    self.sprite = sprites["stage06e01"][7]
    self.x, self.y = x, y
    self.bound = false
    self.layer = LAYER_ENEMY - 1
    self.al = 128
    self.co = {128, 128, 255}
    task.New(self, function()
        calc.LerpTo(self, "al", 0, 60, 0)
        calc.LerpTo(self.co, 1, 0, 60, 0)
        calc.LerpTo(self.co, 2, 0, 60, 0)
        calc.LerpTo(self.co, 3, 255, 60, 0)
        task.Wait(60)
        Del(self)
    end)
end
function ShadowR:frame()
    task.Do(self)
end
function ShadowR:render()
    local sprite = self.sprite
    local x, y, w, h = sprite.x, sprite.y, sprite.w, sprite.h
    local al = self.al
    local co = self.co
    draw.Rect2D(self.tex, "mul+add", Color(al, unpack(co)), {-w / 2, w / 2, -h / 2, h / 2},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, 0)
end

local ShadowL = Class(object)
function ShadowL:init(x, y)
    self.tex = sprites["stage06e01"].tex
    self.sprite = sprites["stage06e01"][11]
    self.x, self.y = x, y
    self.bound = false
    self.layer = LAYER_ENEMY - 1
    self.al = 128
    self.co = {128, 128, 255}
    task.New(self, function()
        calc.LerpTo(self, "al", 0, 60, 0)
        calc.LerpTo(self.co, 1, 0, 60, 0)
        calc.LerpTo(self.co, 2, 0, 60, 0)
        calc.LerpTo(self.co, 3, 255, 60, 0)
        task.Wait(60)
        Del(self)
    end)
end
function ShadowL:frame()
    task.Do(self)
end
function ShadowL:render()
    local sprite = self.sprite
    local x, y, w, h = sprite.x, sprite.y, sprite.w, sprite.h
    local al = self.al
    local co = self.co
    draw.Rect2D(self.tex, "mul+add", Color(al, unpack(co)), {-w / 2, w / 2, -h / 2, h / 2},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, 0)
end

function lib.CreateBossShadow(b, type)
    if type == 1 then
        New(ShadowR, b.x, b.y)
    else
        New(ShadowL, b.x, b.y)
    end
end
------------------------------------------------------------
local BossEye01 = Class(object)
function BossEye01:init(b)
    self.boss = b
    self.layer = LAYER_ENEMY - 4
    self._dx, self._dy = 0, 0
    self.x, self.y = b.x, b.y
    self.bound = false
    self.hs, self.vs = 0, 1
    task.New(self, function()
        task.Wait(30)
        calc.LerpTo(self, "hs", 1, 30, 4)
        task.Wait(30)
        while true do
            calc.LerpTo(self, "hs", 0.95, 48, 4)
            task.Wait(48)
            calc.LerpTo(self, "hs", 1, 48, 4)
            task.Wait(48)
        end
    end)
end
function BossEye01:frame()
    task.Do(self)
    local b = self.boss
    if IsValid(b) then
        self.x, self.y = b.x + self._dx, b.y + self._dy
    else
        Del(self)
    end
end
function BossEye01:render()
    local sprite = sprites["stage06e02"]
    local x, y, w, h = sprite[0].x, sprite[0].y, sprite[0].w, sprite[0].h
    local hs, vs = self.hs, self.vs
    draw.Rect2D(sprite.tex, "", Color(0xFFFFFFFF), {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot or 0)
end

local BossEye02 = Class(object)
function BossEye02:init(b)
    self.boss = b
    self.layer = LAYER_ENEMY - 4
    self._dx, self._dy = -114, -54
    self.x, self.y = b.x + self._dx, b.y + self._dy
    self.bound = false
    self.rot = 0
    self.hs, self.vs = 0, 0
    task.New(self, function()
        task.Wait(60)
        calc.LerpTo(self, "hs", 1, 30, 4)
        calc.LerpTo(self, "vs", 1, 30, 4)
        task.Wait(30)
        while true do
            calc.LerpTo(self, "rot", -2.8125, 48, 9)
            task.Wait(48)
            calc.LerpTo(self, "rot", 2.8125, 48, 9)
            task.Wait(48)
        end
    end)
end
function BossEye02:frame()
    task.Do(self)
    local b = self.boss
    if IsValid(b) then
        self.x, self.y = b.x + self._dx, b.y + self._dy
    else
        Del(self)
    end
end
function BossEye02:render()
    local sprite = sprites["stage06e02"]
    local x, y, w, h = sprite[1].x, sprite[1].y, sprite[1].w, sprite[1].h
    local hs, vs = self.hs, self.vs
    draw.Rect2D(sprite.tex, "", Color(0xFFFFFFFF), {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot or 0)
end

local BossEye03 = Class(object)
function BossEye03:init(b)
    self.boss = b
    self.layer = LAYER_ENEMY - 4
    self._dx, self._dy = 114, -54
    self.x, self.y = b.x + self._dx, b.y + self._dy
    self.bound = false
    self.rot = 0
    self.hs, self.vs = 0, 0
    task.New(self, function()
        task.Wait(60)
        calc.LerpTo(self, "hs", 1, 30, 4)
        calc.LerpTo(self, "vs", 1, 30, 4)
        task.Wait(30)
        while true do
            calc.LerpTo(self, "rot", 2.8125, 48, 9)
            task.Wait(48)
            calc.LerpTo(self, "rot", -2.8125, 48, 9)
            task.Wait(48)
        end
    end)
end
function BossEye03:frame()
    task.Do(self)
    local b = self.boss
    if IsValid(b) then
        self.x, self.y = b.x + self._dx, b.y + self._dy
    else
        Del(self)
    end
end
function BossEye03:render()
    local sprite = sprites["stage06e02"]
    local x, y, w, h = sprite[1].x, sprite[1].y, sprite[1].w, sprite[1].h
    local hs, vs = self.hs, self.vs
    draw.Rect2D(sprite.tex, "", Color(0xFFFFFFFF), {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot or 0)
end

local BossEye04 = Class(object)
function BossEye04:init(b)
    self.boss = b
    self.layer = LAYER_ENEMY - 4
    self._dx, self._dy = -64, 80
    self.x, self.y = b.x + self._dx, b.y + self._dy
    self.bound = false
    self.rot = 0
    self.hs, self.vs = 0, 0
    task.New(self, function()
        task.Wait(60)
        calc.LerpTo(self, "hs", 1, 30, 4)
        calc.LerpTo(self, "vs", 1, 30, 4)
        task.Wait(30)
        while true do
            calc.LerpTo(self, "rot", -2.8125, 48, 9)
            task.Wait(48)
            calc.LerpTo(self, "rot", 2.8125, 48, 9)
            task.Wait(48)
        end
    end)
end
function BossEye04:frame()
    task.Do(self)
    local b = self.boss
    if IsValid(b) then
        self.x, self.y = b.x + self._dx, b.y + self._dy
    else
        Del(self)
    end
end
function BossEye04:render()
    local sprite = sprites["stage06e02"]
    local x, y, w, h = sprite[2].x, sprite[2].y, sprite[2].w, sprite[2].h
    local hs, vs = self.hs, self.vs
    draw.Rect2D(sprite.tex, "", Color(0xFFFFFFFF), {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot or 0)
end

local BossEye05 = Class(object)
function BossEye05:init(b)
    self.boss = b
    self.layer = LAYER_ENEMY - 4
    self._dx, self._dy = 64, 80
    self.x, self.y = b.x + self._dx, b.y + self._dy
    self.bound = false
    self.rot = 0
    self.hs, self.vs = 0, 0
    task.New(self, function()
        task.Wait(60)
        calc.LerpTo(self, "hs", 1, 30, 4)
        calc.LerpTo(self, "vs", 1, 30, 4)
        task.Wait(30)
        while true do
            calc.LerpTo(self, "rot", 2.8125, 48, 9)
            task.Wait(48)
            calc.LerpTo(self, "rot", -2.8125, 48, 9)
            task.Wait(48)
        end
    end)
end
function BossEye05:frame()
    task.Do(self)
    local b = self.boss
    if IsValid(b) then
        self.x, self.y = b.x + self._dx, b.y + self._dy
    else
        Del(self)
    end
end
function BossEye05:render()
    local sprite = sprites["stage06e02"]
    local x, y, w, h = sprite[2].x, sprite[2].y, sprite[2].w, sprite[2].h
    local hs, vs = self.hs, self.vs
    draw.Rect2D(sprite.tex, "", Color(0xFFFFFFFF), {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot or 0)
end

local BossEye06 = Class(object)
function BossEye06:init(b, dx, dy)
    self.boss = b
    self.layer = LAYER_ENEMY - 4
    self._dx, self._dy = dx, dy
    self.rx, self.ry = 0, 0
    self.x, self.y = b.x + self._dx + self.rx, b.y + self._dy + self.ry
    self.bound = false
    self.flag = true
    self.hs, self.vs = 0, 0
    task.New(self, function()
        task.Wait(60)
        calc.LerpTo(self, "hs", 1, 30, 4)
        calc.LerpTo(self, "vs", 1, 30, 4)
        task.Wait(30)
    end)
end
function BossEye06:frame()
    task.Do(self)
    local b = self.boss
    if IsValid(b) then
        self.x, self.y = b.x + self._dx + self.rx, b.y + self._dy + self.ry
    else
        Del(self)
    end
end
function BossEye06:render()
    local sprite = sprites["stage06e02"]
    local x, y, w, h = sprite[3].x, sprite[3].y, sprite[3].w, sprite[3].h
    local hs, vs = self.hs, self.vs
    draw.Rect2D(sprite.tex, "", Color(0xFFFFFFFF), {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot or 0)
end

local BossEye07 = Class(object)
function BossEye07:init(b)
    self.boss = b
    self.layer = LAYER_ENEMY - 4
    self._dx, self._dy = 0, 0
    self.x, self.y = b.x + self._dx, b.y + self._dy
    self.bound = false
    self.rot = -180
    self.hs, self.vs = 0, 0
    task.New(self, function()
        calc.LerpTo(self, "hs", 1, 30, 4)
        calc.LerpTo(self, "vs", 1, 30, 4)
        calc.LerpTo(self, "rot", 0, 30, 4)
        task.Wait(60)
        task.Wait(48)
        while true do
            calc.LerpTo(self, "hs", 0.9, 48, 9)
            calc.LerpTo(self, "vs", 0.9, 48, 9)
            task.Wait(48)
            calc.LerpTo(self, "hs", 1, 48, 9)
            calc.LerpTo(self, "vs", 1, 48, 9)
            task.Wait(48)
        end
    end)
end
function BossEye07:frame()
    task.Do(self)
    local b = self.boss
    if IsValid(b) then
        self.x, self.y = b.x + self._dx, b.y + self._dy
    else
        Del(self)
    end
end
function BossEye07:render()
    local sprite = sprites["stage06e03"]
    local x, y, w, h = sprite[0].x, sprite[0].y, sprite[0].w, sprite[0].h
    local hs, vs = self.hs, self.vs
    draw.Rect2D(sprite.tex, "", Color(0xFFFFFFFF), {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot or 0)
end

function lib.CreateBossEyes(b)
    b.eyes = {}
    table.insert(b.eyes, New(BossEye01, b))
    table.insert(b.eyes, New(BossEye07, b))
    table.insert(b.eyes, New(BossEye06, b, -114, -54))
    table.insert(b.eyes, New(BossEye06, b, 114, -54))
    table.insert(b.eyes, New(BossEye06, b, -64, 80))
    table.insert(b.eyes, New(BossEye06, b, 64, 80))
    table.insert(b.eyes, New(BossEye02, b))
    table.insert(b.eyes, New(BossEye03, b))
    table.insert(b.eyes, New(BossEye04, b))
    table.insert(b.eyes, New(BossEye05, b))
end

function lib.DeleteBossEyes(b)
    for i, v in ipairs(b.eyes) do
        if IsValid(v) then
            Del(v)
        end
    end
end
------------------------------------------------------------
local BossLaser01 = plus.Class(object)
function BossLaser01:init(obj)
    self.obj = obj
    self.sprites = {}
    self.colli = false
    self.x, self.y = obj.x, obj.y
    self.timer = -1
    local script00 = task.New(obj, function()
        self.sprites[1] = {}
        self.sprites[1].hs = 1
        self.sprites[1].vs = 1
        while not self.delete do
            self.sprites[1].sprite = sprites["stage05e02"][0]
            for _ = 1, 2 do
                if self.delete then break end
                task.Wait(1)
            end
            self.sprites[1].sprite = sprites["stage05e02"][1]
            for _ = 1, 2 do
                if self.delete then break end
                task.Wait(1)
            end
        end
        calc.LerpTo(self.sprites[1], "vs", 0, 30, 0)
    end)
    local script01 = task.New(obj, function()
        self.sprites[2] = {}
        self.sprites[2].hs = 1
        self.sprites[2].vs = 0.032
        self.sprites[2].sprite = sprites["stage05e02"][2]
        while not self.colli do
            task.Wait(1)
        end
        local hs, vs = self.sprites[2].hs, self.sprites[2].vs
        for i = 1, 30 do
            if self.delete then break end
            self.sprites[2].hs = func(hs, 1, i / 30, 0)
            self.sprites[2].vs = func(vs, 1, i / 30, 0)
            task.Wait(1)
        end
        while not self.delete do
            task.Wait(1)
        end
        calc.LerpTo(self.sprites[2], "vs", 0, 30, 0)
    end)
end
function BossLaser01:frame()
    local obj = self.obj
    if not IsValid(obj) then return end
    self.x, self.y = obj.x, obj.y
    self.colli = obj.colli
    self.delete = obj.delete
    if self.colli and not(self.delete) then
        self.timer = self.timer + 1
        local w, l = 0.666667 * min(self.timer, 30) , 17.066668 * min(self.timer, 30)
        local p = player
        if IsValid(p) then
            local x, y = (p.x - self.x), (p.y - self.y)
            x, y = calc.Rotate2D(x, y, -obj.rot)
            if x < l + p.a and x > 0 - p.a and y < (w / 2) + p.a and y > (-w / 2) + p.a then
                if p.class.colli then p.class.colli(p, obj) end
            end
            if p.grazer and IsValid(p.grazer) and (obj.timer % 5) == 0 then
                if x < l + p.grazer.a and x > 0 - p.grazer.a and y < w / 2 + p.grazer.a and y > -w / 2 - p.grazer.a then
                    item.PlayerGraze()
                    p.grazer.grazed = true
                end
            end
        end
    end
end
function BossLaser01:render()
    local obj = self.obj
    local tex = sprites["stage05e02"].tex
    if not IsValid(obj) then return end
    local sp = self.sprites[2]
    local hs, vs = sp.hs or 0, sp.vs or 0
    local co = Color(255, 255, 255, 255)
    local rot = obj.rot
    local x, y, w, h = sp.sprite.x, sp.sprite.y, sp.sprite.w, sp.sprite.h
    local tw, th = GetTextureSize(tex)
    x = x + (-0.05 * tw) * obj.timer
    draw.Rect2D(tex, "mul+add", co, {0 * hs, w * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, rot)
    sp = self.sprites[1]
    hs, vs = sp.hs or 0, sp.vs or 0
    co = Color(255, 255, 255, 255)
    x, y, w, h = sp.sprite.x, sp.sprite.y, sp.sprite.w, sp.sprite.h
    draw.Rect2D(tex, "mul+add", co, {0 * hs, w * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, rot)
end

local BossLaser02 = plus.Class(object)
function BossLaser02:init(obj)
    self.obj = obj
    self.sprites = {}
    self.colli = false
    self.x, self.y = obj.x, obj.y
    self.timer = -1
    local script00 = task.New(obj, function()
        self.sprites[1] = {}
        self.sprites[1].hs = 1.5
        self.sprites[1].vs = 1.5
        while not self.delete do
            self.sprites[1].sprite = sprites["stage05e02"][0]
            for _ = 1, 2 do
                if self.delete then break end
                task.Wait(1)
            end
            self.sprites[1].sprite = sprites["stage05e02"][1]
            for _ = 1, 2 do
                if self.delete then break end
                task.Wait(1)
            end
        end
        calc.LerpTo(self.sprites[1], "hs", 1, 30, 0)
        calc.LerpTo(self.sprites[1], "vs", 0, 30, 0)
    end)
    local script01 = task.New(obj, function()
        self.sprites[2] = {}
        self.sprites[2].hs = 0.01
        self.sprites[2].vs = 0
        self.sprites[2].sprite = sprites["stage05e02"][2]
        while not self.colli do
            task.Wait(1)
        end
        local hs, vs = self.sprites[2].hs, self.sprites[2].vs
        for i = 1, 30 do
            if self.delete then break end
            self.sprites[2].hs = func(hs, 1, i / 30, 0)
            self.sprites[2].vs = func(vs, 1.8, i / 30, 0)
            task.Wait(1)
        end
        while not self.delete do
            task.Wait(1)
        end
        calc.LerpTo(self.sprites[2], "vs", 0, 30, 0)
    end)
end
function BossLaser02:frame()
    local obj = self.obj
    if not IsValid(obj) then return end
    self.timer = self.timer + 1
    self.x, self.y = obj.x, obj.y
    self.colli = obj.colli
    self.delete = obj.delete
end
function BossLaser02:render()
    local obj = self.obj
    local tex = sprites["stage05e02"].tex
    if not IsValid(obj) then return end
    local sp = self.sprites[2]
    local hs, vs = sp.hs or 0, sp.vs or 0
    local co = Color(255, 255, 0, 0)
    local rot = obj.rot
    local x, y, w, h = sp.sprite.x, sp.sprite.y, sp.sprite.w, sp.sprite.h
    local tw, th = GetTextureSize(tex)
    x = x + (-0.05 * tw) * obj.timer
    draw.Rect2D(tex, "", co, {0 * hs, w * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, rot)
    sp = self.sprites[1]
    hs, vs = sp.hs or 0, sp.vs or 0
    co = Color(255, 255, 0, 0)
    x, y, w, h = sp.sprite.x, sp.sprite.y, sp.sprite.w, sp.sprite.h
    draw.Rect2D(tex, "", co, {0 * hs, w * hs, -h / 2 * vs, h / 2 * vs},
    {x + 0, x + w, y + h, y + 0}, self.x, self.y, rot)
end

function lib.SetBossLaser(obj, type)
    type = type or 1
    if type == 1 then
        obj.laser = BossLaser01(obj)
    else
        obj.laser = BossLaser02(obj)
    end
end
------------------------------------------------------------
return lib