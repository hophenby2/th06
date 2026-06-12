local calc = require("liu_10_mc.script.liu_10_mc_math")
local func = calc.lerp
local rnd = calc.rnd
local draw = require("liu_10_mc.script.liu_10_mc_draw")
------------------------------------------------------------------
local lib = {}
------------------------------------------------------------------
local function LoadTexResouces()
    local dir = "liu_10_mc/img/bullet/"
    LoadTexture("liu_10_mc_eff01", dir .. "liu_10_mc_eff01.png")
    if not lstg.CheckRes(1, "liu_10_mc_etama2") then
        LoadTexture("liu_10_mc_etama2", dir .. "liu_10_mc_etama2.png")
    end
    LoadTexture("liu_10_mc_etama3", dir .. "liu_10_mc_etama3.png")
end
lib.LoadTexResouces = LoadTexResouces
------------------------------------------------------------------
local sprites = {
    ["eff_aura"] = {
        tex = "liu_10_mc_eff01",
        [0] = {x = 0, y = 0, w = 48, h = 48},
        [1] = {x = 48, y = 0, w = 48, h = 48},
    },
    ["eff_line"] = {
        tex = "liu_10_mc_etama3",
        [0] = {x = 65, y = 0, w = 14, h = 128},
        [1] = {x = 81, y = 0, w = 14, h = 128},
        [2] = {x = 49, y = 0, w = 14, h = 128},
        [3] = {x = 49, y = 0, w = 14, h = 128},
        [4] = {x = 33, y = 0, w = 14, h = 295},
        [5] = {x = 97, y = 0, w = 14, h = 128},
    },
    ["eff_maple"] = {
        tex = "liu_10_mc_etama2",
        [0] = {x = 0, y = 224, w = 32, h = 32},
        [1] = {x = 33, y = 225, w = 30, h = 30},
    },
    ["eff_magicsquare"] = {
        tex = "liu_10_mc_etama2",
        [0] = {x = 128, y = 80, w = 128, h = 128},
    },
    ["eff_deadcircle"] = {
        tex = "liu_10_mc_etama2",
        [0] = {x = 128, y = 16, w = 64, h = 64},
        [1] = {x = 192, y = 16, w = 64, h = 64},
        [2] = {x = 0, y = 80, w = 64, h = 64},
        [3] = {x = 64, y = 80, w = 64, h = 64},
    }
}
------------------------------------------------------------------
--- eff_aura
local eff_aura = Class(object)
local eff_aura_obj1 = Class(object)
local eff_aura_obj2 = Class(object)
local eff_aura_obj3 = Class(object)

function eff_aura:init(b)
    self.boss = b
    self.group = GROUP_GHOST
    self.time = - 1
end
function eff_aura:frame()
    self.time = self.time + 1
    local b = self.boss
    if IsValid(b) then
        if self.time == 0 then
            New(eff_aura_obj1, b)
        elseif self.time == 3 then
            New(eff_aura_obj2, b)
        elseif self.time == 4 then
            New(eff_aura_obj3, b)
        elseif self.time == 6 then
            self.time = -1
        end
    else
        Del(self)
    end
end

function eff_aura_obj1:init(b)
    self.layer = LAYER_ENEMY - 5
    self.group = GROUP_GHOST
    self.boss = b
    self.tex = sprites["eff_aura"].tex
    self.pos = {ran:Float(-1, 1) * 4, 0}
    self.scale = {ran:Float(0, 1) * 0.7 + 1, 0}
    self.ts = {self.scale[1], ran:Float(0, 1) * 0.5 + 1.9}
    self.alpha = 255
end
function eff_aura_obj1:frame()
    local t = self.timer
    self.hscale = func(self.scale[1], self.ts[1], min(t / 30, 1), 4)
    self.vscale = func(self.scale[2], self.ts[2], min(t / 30, 1), 4)
    self.alpha = func(255, 0, min(t / 30, 1), 1)
    local b = self.boss
    if IsValid(b) then
        self.x = b.x + self.pos[1]
        self.y = b.y + self.pos[2]
    else
        Del(self)
    end
    if self.timer >= 30 then
        Del(self)
    end
end
function eff_aura_obj1:render()
    local sprite = sprites["eff_aura"][0]
    local x, y, w, h = sprite.x, sprite.y, sprite.w, sprite.h
    local hs, vs = self.hscale, self.vscale
    draw.Rect2D(self.tex, "mul+add", Color(self.alpha, 128, 32, 32),
    {-w / 2 * hs, w / 2 * hs, 0 * vs, h * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, 0)
end

function eff_aura_obj2:init(b)
    self.layer = LAYER_BG + 3
    self.group = GROUP_GHOST
    self.boss = b
    self.tex = sprites["eff_aura"].tex
    local s = ran:Float(0, 1) * 0.7 + 1.6
    self.scale = {s, s}
    self.ts = {0.7, 0.7}
    self.rot = ran:Float(-180, 180)
    self.alpha = 0
end
function eff_aura_obj2:frame()
    local t = self.timer
    self.hscale = func(self.scale[1], self.ts[1], min(t / 30, 1), 4)
    self.vscale = func(self.scale[2], self.ts[2], min(t / 30, 1), 4)
    self.alpha = func(0, 255, min(t / 30, 1), 4)
    local b = self.boss
    if IsValid(b) then
        self.x = b.x
        self.y = b.y
    else
        Del(self)
    end
    if self.timer >= 30 then
        Del(self)
    end
end
function eff_aura_obj2:render()
    local sprite = sprites["eff_aura"][1]
    local x, y, w, h = sprite.x, sprite.y, sprite.w, sprite.h
    local hs, vs = self.hscale, self.vscale
    draw.Rect2D(self.tex, "mul+add", Color(self.alpha, 128, 0, 0),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, 0)
end

function eff_aura_obj3:init(b)
    self.layer = LAYER_ENEMY - 5
    self.boss = b
    self.tex = sprites["eff_aura"].tex
    local s = ran:Float(0, 1) * 0.7 + 2
    self.scale = {s, s}
    self.ts = {1.2, 1.2}
    self.rot = ran:Float(-180, 180)
    self.alpha = 0
end
function eff_aura_obj3:frame()
    local t = self.timer
    self.hscale = func(self.scale[1], self.ts[1], min(t / 30, 1), 4)
    self.vscale = func(self.scale[2], self.ts[2], min(t / 30, 1), 4)
    self.alpha = func(0, 64, min(t / 30, 1), 4)
    local b = self.boss
    if IsValid(b) then
        self.x = b.x
        self.y = b.y
    else
        Del(self)
    end
    if self.timer >= 30 then
        Del(self)
    end
end
function eff_aura_obj3:render()
    local sprite = sprites["eff_aura"][1]
    local x, y, w, h = sprite.x, sprite.y, sprite.w, sprite.h
    local hs, vs = self.hscale, self.vscale
    draw.Rect2D(self.tex, "mul+add", Color(self.alpha, 255, 255, 255),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, 0)
end

lib.SetEffAura = function(b)
    b.eff_aura = New(eff_aura, b)
end
------------------------------------------------------------------
--- eff_magicsquare
local eff_magicsquare = Class(object)
function eff_magicsquare:init(b)
    self.boss = b
    self.layer = LAYER_ENEMY - 5
    self.group = GROUP_GHOST
    self.bound = false
    self.x, self.y = b.x, b.y
    self.rot = -180
    self.alpha = 128
    self.scale = 0
    self.omiga = 0
    task.New(self, function()
        calc.LerpTo(self, "rot", 180, 60, 4)
        calc.LerpTo(self, "scale", 2, 60, 4)
        task.Wait(60)
        self.omiga = 5.625
        while true do
            calc.LerpTo(self, "scale", 1.6, 60, 9)
            calc.LerpTo(self, "alpha", 128, 60, 9)
            task.Wait(60)
            calc.LerpTo(self, "scale", 2, 60, 9)
            calc.LerpTo(self, "alpha", 96, 60, 9)
            task.Wait(60)
        end
    end)
end
function eff_magicsquare:frame()
    task.Do(self)
    local b = self.boss
    if IsValid(b) then
        self.x, self.y = b.x, b.y
    else
        Del(self)
    end
end
function eff_magicsquare:render()
    local sprite = sprites["eff_magicsquare"]
    local x, y, w, h = sprite[0].x, sprite[0].y, sprite[0].w, sprite[0].h
    local hs, vs = self.scale, self.scale
    draw.Rect2D(sprite.tex, "mul+add", Color(self.alpha, 255, 255, 255),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot)
end

lib.SetEffMagicsquare = function(b)
    b.eff_magicsquare = New(eff_magicsquare, b)
end
------------------------------------------------------------------
--- enm_kill
local enm_kill_circle01 = Class(object)
function enm_kill_circle01:init(x, y, index)
    self.layer = LAYER_ENEMY_BULLET_EF
    self.group = GROUP_GHOST
    self.x, self.y = x, y
    self.index = index
    self.hscale, self.vscale = 0.2, 0.2
    self.alpha = 255
    task.New(self, function()
        calc.LerpTo(self, "hscale", 2.5, 30, 4)
        calc.LerpTo(self, "vscale", 2.5, 30, 4)
        calc.LerpTo(self, "alpha", 0, 30, 4)
        task.Wait(30)
        Del(self)
    end)
end
function enm_kill_circle01:frame()
    task.Do(self)
end
function enm_kill_circle01:render()
    local sprite = sprites["eff_deadcircle"]
    local x, y, w, h = sprite[self.index].x, sprite[self.index].y, sprite[self.index].w, sprite[self.index].h
    local hs, vs = self.hscale, self.vscale
    draw.Rect2D(sprite.tex, "mul+add", Color(self.alpha, 255, 255, 255),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, 0)
end

local enm_kill_circle02 = Class(object)
function enm_kill_circle02:init(x, y, index)
    self.layer = LAYER_ENEMY_BULLET_EF
    self.group = GROUP_GHOST
    self.x, self.y = x, y
    self.index = index
    self.rot = rnd.Float(-180, 180)
    self.hscale, self.vscale = 0.5, 0.5
    self.alpha = 255
    task.New(self, function()
        calc.LerpTo(self, "hscale", 3.5, 30, 4)
        calc.LerpTo(self, "vscale", 0.2, 30, 4)
        calc.LerpTo(self, "alpha", 0, 30, 4)
        task.Wait(30)
        Del(self)
    end)
end
function enm_kill_circle02:frame()
    task.Do(self)
end
function enm_kill_circle02:render()
    local sprite = sprites["eff_deadcircle"]
    local x, y, w, h = sprite[self.index].x, sprite[self.index].y, sprite[self.index].w, sprite[self.index].h
    local hs, vs = self.hscale, self.vscale
    draw.Rect2D(sprite.tex, "mul+add", Color(self.alpha, 255, 255, 255),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.rot)
end

local enm_kill_maple = Class(object)
function enm_kill_maple:init(x, y)
    self.layer = LAYER_ENEMY_BULLET_EF
    self.group = GROUP_GHOST
    self.x, self.y = x, y
    local t = rnd.Int(0, 15) + 20
    local s = rnd.Float(0, 1) * 1.5 + 0.5
    local ra = rnd.Float(-180, 180)
    local r = rnd.Float(0, 1) * 256
    local rx, ry = cos(ra) * r, sin(ra) * r
    self.alpha = 64
    self.scale = s
    task.New(self, function()
        calc.LerpTo(self, "x", x + rx, t, 4)
        calc.LerpTo(self, "y", y + ry, t, 4)
        calc.LerpTo(self, "scale", 0, t, 4)
        task.Wait(t)
        Del(self)
    end)
end
function enm_kill_maple:frame()
    task.Do(self)
end
function enm_kill_maple:render()
    local sprite = sprites["eff_maple"]
    local x, y, w, h = sprite[0].x, sprite[0].y, sprite[0].w, sprite[0].h
    local hs, vs = self.scale, self.scale
    draw.Rect2D(sprite.tex, "mul+add", Color(self.alpha, 255, 255, 255),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, 0)
end

lib.CreateEnmKillEffect = function(b, index)
    New(enm_kill_circle01, b.x, b.y, index)
    New(enm_kill_circle02, b.x, b.y, index)
    for _ = 1, 7 do
        New(enm_kill_maple, b.x, b.y)
    end
end
------------------------------------------------------------------
--- change_eff
local change_eff_maple = Class(object)
function change_eff_maple:init(x, y)
    self.layer = LAYER_ENEMY_BULLET_EF + 2
    self.group = GROUP_GHOST
    self.bound = false
    self.omiga = rnd.Float(-180, 180) / 32
    local s = rnd.Float(0, 1) * 3 + 1
    self.scale = s
    local ra = rnd.Float(-180, 180)
    local rx, ry = cos(ra) * 256, sin(ra) * 256
    self.x, self.y = x + rx, y + ry
    self.alpha = 0
    task.New(self, function()
        calc.LerpTo(self, "x", x, 60, 4)
        calc.LerpTo(self, "y", y, 60, 4)
        calc.LerpTo(self, "alpha", 128, 20, 4)
        task.Wait(20)
        calc.LerpTo(self, "alpha", 0, 20, 1)
        calc.LerpTo(self, "scale", 0, 20, 1)
        task.Wait(20)
        Del(self)
    end)
end
function change_eff_maple:frame()
    task.Do(self)
    self.rot = self.rot + self.omiga
end
function change_eff_maple:render()
    local sprite = sprites["eff_maple"]
    local x, y, w, h = sprite[1].x, sprite[1].y, sprite[1].w, sprite[1].h
    local hs, vs = self.scale, self.scale
    draw.Rect2D(sprite.tex, "mul+add", Color(self.alpha, 255, 255, 255),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.omiga)
end

local change_eff_circle = Class(object)
function change_eff_circle:init(x, y)
    self.layer = LAYER_ENEMY_BULLET_EF + 1
    self.group = GROUP_GHOST
    self.x, self.y = x, y
    self.bound = false
    self.r, self.n = 256, 48
    self.scale = 1
    self.al2, self.co2 = 1, {255, 80, 80}
    self.al1, self.co1 = 0, {255, 255, 192}
    task.New(self, function()
        calc.LerpTo(self, "al1", 255, 20, 0)
        task.Wait(20)
        calc.LerpTo(self, "al2", 255, 40, 0)
        calc.LerpTo(self, "al1", 0, 20, 0)
        calc.LerpTo(self, "scale", 0, 40, 0)
        task.Wait(40)
        Del(self)
    end)
end
function change_eff_circle:frame()
    task.Do(self)
end
function change_eff_circle:render()
    local c1, c2 = Color(self.al1, unpack(self.co1)), Color(self.al2, unpack(self.co2))
    draw.drawPoly("mul+add", c1, self.x, self.y, self.r * self.scale, self.n, 0, c2)
end

local change_eff = Class(object)
function change_eff:init(b)
    self.group = GROUP_GHOST
    self.x, self.y = b.x, b.y
    New(change_eff_circle, self.x, self.y)
    task.New(self, function()
        for _ = 1, 30 do
            New(change_eff_maple, self.x, self.y)
            task.Wait(1)
        end
        Del(self)
    end)
end
function change_eff:frame()
    task.Do(self)
    self.rot = self.rot + self.omiga
end

lib.ChangeEff = function(b)
    New(change_eff, b)
end
------------------------------------------------------------------
--- BossDead
local boss_dead_maple = Class(object)
function boss_dead_maple:init(x, y)
    self.layer = LAYER_ENEMY_BULLET_EF + 2
    self.group = GROUP_GHOST
    self.bound = false
    self.omiga = rnd.Float(-180, 180) / 32
    local s = rnd.Float(0, 1) * 3 + 1
    self.scale = s
    self.x, self.y = x, y
    local ra = rnd.Float(-180, 180)
    local rx, ry = cos(ra) * 256, sin(ra) * 256
    ra = rnd.Float(-180, 180)
    local rx2, ry2 = cos(ra) * 512, sin(ra) * 512
    self.alpha = 0
    task.New(self, function()
        task.New(self, function()
            local xx, yy = self.x, self.y
            for i = 1, 90 do
                self.x = calc.bezier(i / 90, xx, xx + rx2, xx + 0, xx + rx)
                self.y = calc.bezier(i / 90, yy, yy + ry2, yy + 0, yy + ry)
                task.Wait(1)
            end
        end)
        calc.LerpTo(self, "alpha", 128, 30, 4)
        task.Wait(60)
        calc.LerpTo(self, "alpha", 0, 30, 1)
        calc.LerpTo(self, "scale", 0, 30, 1)
        task.Wait(30)
        Del(self)
    end)
end
function boss_dead_maple:frame()
    task.Do(self)
    self.rot = self.rot + self.omiga
end
function boss_dead_maple:render()
    local sprite = sprites["eff_maple"]
    local x, y, w, h = sprite[1].x, sprite[1].y, sprite[1].w, sprite[1].h
    local hs, vs = self.scale, self.scale
    draw.Rect2D(sprite.tex, "mul+add", Color(self.alpha, 255, 255, 255),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, self.omiga)
end

local boss_dead_eff01 = Class(object)
function boss_dead_eff01:init(x, y)
    task.New(self, function()
        for _ = 1, 30 do
            New(boss_dead_maple, x, y)
            task.Wait(2)
        end
        Del(self)
    end)
end
function boss_dead_eff01:frame()
    task.Do(self)
end

local boss_dead_eff02 = Class(object)
function boss_dead_eff02:init(x, y)
    task.New(self, function()
        for _ = 1, 60 do
            New(boss_dead_maple, x, y)
        end
        Del(self)
    end)
end
function boss_dead_eff02:frame()
    task.Do(self)
end

local boss_dead_circle = Class(object)
function boss_dead_circle:init(x, y)
    self.layer = LAYER_ENEMY_BULLET_EF
    self.group = GROUP_GHOST
    self.x, self.y = x, y
    self.hscale, self.vscale = 0.5, 0.5
    self.alpha = 255
    task.New(self, function()
        calc.LerpTo(self, "hscale", 5.5, 30, 4)
        calc.LerpTo(self, "vscale", 5.5, 30, 4)
        calc.LerpTo(self, "alpha", 0, 30, 4)
        task.Wait(30)
        Del(self)
    end)
end
function boss_dead_circle:frame()
    task.Do(self)
end
function boss_dead_circle:render()
    local sprite = sprites["eff_deadcircle"]
    local x, y, w, h = sprite[0].x, sprite[0].y, sprite[0].w, sprite[0].h
    local hs, vs = self.hscale, self.vscale
    draw.Rect2D(sprite.tex, "mul+add", Color(self.alpha, 255, 255, 255),
    {-w / 2 * hs, w / 2 * hs, -h / 2 * vs, h / 2 * vs}, {x + 0, x + w, y + h, y + 0}, self.x, self.y, 0)
end

function lib.boss_explode(self)
    local system = self._bosssys
    function system:explode()
        local b = self.boss
        local card = b.current_card
        local angle = ran:Float(-15, 15)
        local sign, v = ran:Sign(), 1.5
        b.is_exploding = true
        b.killed = true
        b.no_killeff = true
        PlaySound("enep01", 0.5)
        b._colli = false
        b.hp = 0
        b.lr = sign * 28
        b.vx = sign * v * cos(angle)
        b.vy = v * sin(angle)
        if not b.timeout then
            New(bullet_cleaner, b.x, b.y, 3000, 120, 60, true, true, 0)
        else
            New(bullet_cleaner, b.x, b.y, 3000, 120, 60, false, true, 0)
        end
        if b.protectPlayer then
            player.protect = 120
        end
        task.New(b, function()
            New(boss_dead_circle, b.x, b.y)
            New(boss_dead_eff01, b.x, b.y)
            for _ = 1, 60 do
                v = v * 0.98
                b.vx = sign * v * cos(angle)
                b.vy = v * sin(angle)
                b.hp = 0
                b.timer = b.timer - 1
                task.Wait(1)
            end
            misc.ShakeScreen(30, 12)
            New(boss_dead_circle, b.x, b.y)
            New(boss_dead_eff02, b.x, b.y)
            self:popSpellResult()
            self:popResult(true)
            self:refresh(1)
            if card and card.after then
                task.New(b, function()
                    card.after(b)
                    Del(b)
                end)
                self:doTask()
            else
                Del(b)
            end
        end)
    end
    function system:slow_explode()
        local b = self.boss
        local card = b.current_card
        local clock = self.clock
        local angle = ran:Float(-15, 15)
        local sign, v = ran:Sign(), 1.5
        b.is_exploding = true
        b.killed = true
        b.no_killeff = true
        PlaySound("enep01", 0.5)
        b._colli = false
        b.hp = 0
        b.lr = sign * 28
        b.vx = sign * v * cos(angle)
        b.vy = v * sin(angle)
        if not b.timeout then
            New(bullet_cleaner, b.x, b.y, 3000, 120, 60, true, true, 0)
        else
            New(bullet_cleaner, b.x, b.y, 3000, 120, 60, false, true, 0)
        end
        clock:Pause()
        lstg.var.timeslow = 4
        if b.protectPlayer then
            player.protect = 120
        end
        task.New(b, function()
            New(boss_dead_circle, b.x, b.y)
            New(boss_dead_eff01, b.x, b.y)
            for _ = 1, 60 do
                v = v * 0.98
                b.vx = sign * v * cos(angle)
                b.vy = v * sin(angle)
                b.hp = 0
                b.timer = b.timer - 1
                task.Wait(1)
            end
            misc.ShakeScreen(30, 12)
            New(boss_dead_circle, b.x, b.y)
            New(boss_dead_eff02, b.x, b.y)
            lstg.var.timeslow = nil
            self:popSpellResult()
            self:popResult(true)
            self:refresh(1)
            if card and card.after then
                task.New(b, function()
                    card.after(b)
                    Del(b)
                end)
                self:doTask()
            else
                Del(b)
            end
        end)
    end
end
------------------------------------------------------------------
return lib