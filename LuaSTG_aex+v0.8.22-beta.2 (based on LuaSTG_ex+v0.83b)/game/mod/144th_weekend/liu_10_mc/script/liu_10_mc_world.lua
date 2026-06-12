local calc = require("liu_10_mc.script.liu_10_mc_math")
local func = calc.lerp
------------------------------------------------------------------
local world = Class(object)
function world:init()
    background.init(self, false)
    --------------------------------------------------------------
    local path = "liu_10_mc/img/background/"
    local tex_list = {
        {"liu_10_mc_stage05a", path .. "liu_10_mc_stage05a.png", true},
        {"liu_10_mc_stage06a", path .. "liu_10_mc_stage06a.png", true},
        {"liu_10_mc_stage06b", path .. "liu_10_mc_stage06b.png", true},
        {"liu_10_mc_stage06c", path .. "liu_10_mc_stage06c.png", true},
        {"liu_10_mc_stage06d", path .. "liu_10_mc_stage06d.png", true},
        {"liu_10_mc_stage06e", path .. "liu_10_mc_stage06e.png", true},
    }
    --------------------------------------------------------------
    self.tex = {}
    for i = 1, #tex_list do
        local p = tex_list[i]
        LoadTexture(p[1], p[2], p[3])
        SetTextureSamplerState(p[1], "linear+wrap")
        self.tex[i] = p[1]
    end
    --------------------------------------------------------------
    Set3D("up", 0.0, 1.0, 0.0)
    Set3D("fovy", 0.5235988)
    Set3D("eye", 0.0, 50.0, -700.0)
    self.at = {0.0, 500.0, 250.0}
    Set3D("fog", 800.0, 1000.0, Color(0xFF000000))
    Set3D("z", 0.1, 5120)
    --------------------------------------------------------------
    self.time = -1
end
function world:frame()
    --------------------------------------------------------------
    self.time = self.time + 1
    if self.time >= 0 and self.time < 2048 then
        local t = self.time
        Set3D("eye", 0.0, func(50.0, 562.0, min(t / 2048, 1), 0), -700.0)
    elseif self.time >= 2048 then
        self.time = 0 - 1
    end
    --------------------------------------------------------------
    for i = 1, #self.at do
        lstg.view3d.at[i] = lstg.view3d.eye[i] + self.at[i]
    end
end
--------------------------------------------------------------
local function render_entry0(self)
    SetViewMode("3d")
    local t = self.ani
    local tex = self.tex[2]
    for i = 0, 7 do
        local _x, _y, _z = 0, 512 * i, 0
        local dx, dy, dz = 0, 0, -250
        local x, y, z = _x + dx, _y + dy, _z + dz
        local scrollX, scrollY = 0, t * (512 * (0.0001))
        local tx, ty, tw, th = 192 + scrollX, 0 + scrollY, 512, 512
        local w, h = 512, 512
        local c = Color(255, 255, 255, 255)
        RenderTexture(tex, "mul+add",
            {x - (w / 2), y + (h / 2), z, tx, ty, c},
            {x + (w / 2), y + (h / 2), z, tx + tw, ty, c},
            {x + (w / 2), y - (h / 2), z, tx + tw, ty + th, c},
            {x - (w / 2), y - (h / 2), z, tx, ty + th, c})
    end
end
--------------------------------------------------------------
local function render_entry1(self)
    SetViewMode("3d")
    local tex = self.tex[1]
    for i = 0, 7 do
        local _x, _y, _z = 0, 512 * i, 0
        local dx, dy, dz = 0, 0, 0
        local x, y, z = _x + dx, _y + dy, _z + dz
        local tx, ty, tw, th = 0, 0, 1024, 512
        local w, h = 1024, 512
        local c = Color(255, 255, 255, 255)
        RenderTexture(tex, "",
            {x - (w / 2), y - (h / 2), z, tx, ty, c},
            {x + (w / 2), y - (h / 2), z, tx + tw, ty, c},
            {x + (w / 2), y + (h / 2), z, tx + tw, ty + th, c},
            {x - (w / 2), y + (h / 2), z, tx, ty + th, c})
    end
end
------------------------------------------------------------------
local function render_entry2(self)
    SetViewMode("3d")
    local t = self.ani
    local tex = self.tex[3]
    for i = 0, 7 do
        local _x, _y, _z = 0, 512 * i, 0
        local dx, dy, dz = 0, 0, -150
        local x, y, z = _x + dx, _y + dy, _z + dz
        local scrollX, scrollY = t * (256 * (0.0002)), 0
        local tx, ty, tw, th = 0 + scrollX, 0 + scrollY, 512, 512
        local w, h = 512, 512
        local c = Color(255, 255, 255, 255)
        RenderTexture(tex, "mul+add",
            {x - (w / 2), y + (h / 2), z, tx, ty, c},
            {x + (w / 2), y + (h / 2), z, tx + tw, ty, c},
            {x + (w / 2), y - (h / 2), z, tx + tw, ty + th, c},
            {x - (w / 2), y - (h / 2), z, tx, ty + th, c})
    end
end
------------------------------------------------------------------
local function render_entry3(self)
    SetViewMode("3d")
    local t = self.ani
    local tex = self.tex[3]
    for i = 0, 7 do
        local _x, _y, _z = 0, 512 * i, 0
        local dx, dy, dz = 0, 0, -100
        local x, y, z = _x + dx, _y + dy, _z + dz
        local scrollX, scrollY = t * (256 * (-0.0001)), 0
        local tx, ty, tw, th = 0 + scrollX, 0 + scrollY, 512, 512
        local w, h = 512, 512
        local al = 64
        if self.ani >= 600 then
            local ani = self.ani - 600
            al = func(64, 255, min(ani / 200, 1), 0)
        end
        local c = Color(al, 255, 255, 255)
        RenderTexture(tex, "mul+add",
            {x - (w / 2), y + (h / 2), z, tx, ty, c},
            {x + (w / 2), y + (h / 2), z, tx + tw, ty, c},
            {x + (w / 2), y - (h / 2), z, tx + tw, ty + th, c},
            {x - (w / 2), y - (h / 2), z, tx, ty + th, c})
    end
end
------------------------------------------------------------------
local function render_sprite0(self)
    SetViewMode("world")
    local tex = self.tex[4]
    local x, y = -192, 224
    local tx, ty, tw, th = 0, 0, 384, 210
    local w, h = tw, th
    local c = Color(255, 255, 255, 255)
    RenderTexture(tex, "",
        {x, y, 0.5, tx, ty, c},
        {x + w, y, 0.5, tx + tw, ty, c},
        {x + w, y - h, 0.5, tx + tw, ty + th, c},
        {x, y - h, 0.5, tx, ty + th, c})
end
------------------------------------------------------------------
local function render_sprite1(self)
    SetViewMode("world")
    local t = self.ani
    local tex = self.tex[5]
    local x, y = -192, 224
    local scrollX, scrollY = t * (512 * (-0.0008)), 0
    local tx, ty, tw, th = 0 + scrollX, 0 + scrollY, 384, 210
    local w, h = tw, th
    local c = Color(192, 255, 255, 255)
    RenderTexture(tex, "mul+rev",
        {x, y, 0.5, tx, ty, c},
        {x + w, y, 0.5, tx + tw, ty, c},
        {x + w, y - h, 0.5, tx + tw, ty + th, c},
        {x, y - h, 0.5, tx, ty + th, c})
end
------------------------------------------------------------------
local function render_sprite2(self)
    SetViewMode("world")
    local t = self.ani
    local tex = self.tex[5]
    local x, y = -192, 224
    local scrollX, scrollY = t * (512 * (-0.0008)), 0
    local tx, ty, tw, th = 0 + scrollX, 100 + scrollY, 384, 210
    local w, h = tw, th
    local c = Color(192, 255, 255, 255)
    RenderTexture(tex, "mul+rev",
        {x, y, 0.5, tx, ty, c},
        {x + w, y, 0.5, tx + tw, ty, c},
        {x + w, y - h, 0.5, tx + tw, ty + th, c},
        {x, y - h, 0.5, tx, ty + th, c})
end
------------------------------------------------------------------
local function render_sprite3(self)
    SetViewMode("world")
    local tex = self.tex[6]
    local x, y = -192, 224
    local tx, ty, tw, th = 0, 0, 384, 210
    local w, h = tw, th
    local c = Color(192, 255, 255, 255)
    RenderTexture(tex, "mul+add",
        {x, y, 0.5, tx, ty, c},
        {x + w, y, 0.5, tx + tw, ty, c},
        {x + w, y - h, 0.5, tx + tw, ty + th, c},
        {x, y - h, 0.5, tx, ty + th, c})
end
------------------------------------------------------------------
function world:render()
    SetViewMode("3d")
    background.WarpEffectCapture()
    ----------------------------------------------
    render_entry1(self)
    render_entry3(self)
    render_entry2(self)
    render_entry0(self)
    render_sprite0(self)
    render_sprite1(self)
    render_sprite2(self)
    render_sprite3(self)
    ----------------------------------------------

    background.WarpEffectApply()
    SetViewMode("world")
end
------------------------------------------------------------------
return world