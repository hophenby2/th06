local draw = require("liu_10_mc.script.liu_10_mc_draw")
-------------------------------------------------------
local texname = {
    "liu_10_mc_screen_world_tex_1",
    "liu_10_mc_screen_world_tex_2",
}
for _, name in ipairs(texname) do
    CreateRenderTarget(name)
    SetTextureSamplerState(name, "point+wrap")
end
-------------------------------------------------------
local function SetViewMode_ScaleWorld()
    local function setViewportAndScissorRect(l,r,b,t)
        SetViewport(l, r, b, t)
        SetScissorRect(l, r, b, t)
    end
    local w, h = setting.resx, setting.resy
    SetOrtho(0, w, 0, h)
    setViewportAndScissorRect(
        0 + screen.dx,
        w + screen.dx,
        0 + screen.dy,
        h + screen.dy
    )
    SetFog()
    SetImageScale(1)
end
-------------------------------------------------------
local _objPush = Class(object)
local _objPop = Class(object)

function _objPush:init()
    self.layer = LAYER_BG - 102
    self.group = GROUP_GHOST
end
function _objPush:render()
    PushRenderTarget(texname[1])
    RenderClear(Color(0, 0, 0, 0))
end

function _objPop:init()
    self.layer = LAYER_TOP + 0.9
    self.group = GROUP_GHOST
    New(_objPush)
end

local function drawTexture()
    local w = lstg.world
    local canvas = {w = 640, h = 480}
    local _w, _h = w.r - w.l, w.t - w.b
    local s = screen.scale
    local dx, dy = screen.dx, screen.dy
    local c = Color(255, 255, 255, 255)
    local _w1, _h1 = _w * s, _h * s
    local bx, by = w.scrl * s + dx, (canvas.h - w.scrt) * s + dy
    local x, y = (w.scrl * s) + (_w1 / 2), (w.scrt * s) - (_h1 / 2)
    SetViewMode_ScaleWorld()
    draw.Rect2D(texname[1], "one", c, {-_w / 2, _w / 2, -_h / 2, _h / 2}, {bx + 0, bx + _w1, by + _h1, by + 0}, x, y, 0)
    SetViewMode("world")
end

function _objPop:render()
    PopRenderTarget()
    PushRenderTarget(texname[2])
    RenderClear(Color(0, 0, 0, 0))
    drawTexture()
    PopRenderTarget()
    local w = lstg.world
    local canvas = {w = 640, h = 480}
    local _w, _h = w.r - w.l, w.t - w.b
    local s = screen.scale
    local dx, dy = screen.dx, screen.dy
    local c = Color(255, 255, 255, 255)
    local _w1, _h1 = _w, _h
    local bx, by = w.scrl * s + (_w1 / 2 * s) + dx, (canvas.h - w.scrt) * s + (_h1 / 2 * s) + dy
    local x, y = (w.scrl * s) + (_w1 / 2 * s), (w.scrt * s) - (_h1 / 2 * s)
    SetViewMode_ScaleWorld()
    draw.Rect2D(texname[2], "one", c, {-_w / 2 * s, _w / 2 * s, -_h / 2 * s, _h / 2 * s}, {bx - (_w1 / 2), bx + (_w1 / 2), by + (_h1 / 2), by - (_h1 / 2)}, x, y, 0)
    SetViewMode("world")
end
-------------------------------------------------------
function liu_10_mc_screen()
    New(_objPop)
end