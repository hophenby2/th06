local draw = require("liu_10_mc.script.liu_10_mc_draw")
local mirror = require("liu_10_mc.script.liu_10_mc_mirrorTexture")
---------------------------------------------
local lib = {}

local function anchor(h, v)
    local x, y = {-0.5, 0.5}, {-0.5, 0.5}
    if h == 1 then
        x = {0, 1}
    elseif h == 2 then
        x = {-1, 0}
    end
    if v == 1 then
        y = {-1, 0}
    elseif v == 2 then
        y = {0, 1}
    end
    return {x[1], x[2], y[1], y[2]}
end

lib.AddLayer = function(obj, tex, sprite, x, y, sx, sy, rot, omiga, blend, scale, cdbg_f, align, c1, is_mirror)
    _spellcard_background.AddLayer(obj, "img_void", false, x, y, rot, 0, 0, omiga, blend, scale[1], scale[2],
        function(self)
            self.task = {}
            self.a, self.r, self.g, self.b = c1:ARGB()
            self.t = 0
            if is_mirror then
                self.m_tex = mirror.CreateMirrorTexture(tex)
            end
        end, cdbg_f,
        function(self)
            local t = self.timer
            if is_mirror then
                mirror.CaptureTexture(tex)
                tex = self.m_tex
            end
            local texSize = {GetTextureSize(tex)}
            local su, sv = sx * texSize[1] * t, sy * texSize[2] * t
            local source = {sprite[1] + su, sprite[1] + su + sprite[3], sprite[2] + sv + sprite[4], sprite[2] + sv}
            local align_s = anchor(unpack(align))
            local hs, vs = self.hscale, self.vscale
            local dest = {sprite[3] * align_s[1] * hs, sprite[3] * align_s[2] * hs, sprite[4] * align_s[3] * vs, sprite[4] * align_s[4] * vs}
            c1 = Color(self._cur_alpha * self.a, self.r, self.g, self.b)
            rot = self.rot
            draw.RectGrad2D(tex, blend, c1, c1, dest, source, x, y, rot)
        end)
end

lib.AddLayerCircle = function(obj, tex, sprite, x, y, sx, sy, rot, omiga, blend, r, rw, n, m, cdbg_f, c1, c2, is_mirror)
    c2 = c2 or c1
    _spellcard_background.AddLayer(obj, "img_void", false, x, y, rot, 0, 0, omiga, blend, 1, 1,
        function(self)
            self.task = {}
            self.a, self.r, self.g, self.b = c1:ARGB()
            self.t = 0
            if is_mirror then
                self.m_tex = mirror.CreateMirrorTexture(tex)
            end
        end, cdbg_f,
        function(self)
            local t = self.timer
            if is_mirror then
                mirror.CaptureTexture(tex)
                tex = self.m_tex
            end
            local texSize = {GetTextureSize(tex)}
            local su, sv = sx * texSize[1] * t, sy * texSize[2] * t
            local source = {sprite[1] + su, sprite[1] + su + sprite[3], sprite[2] + sv + sprite[4], sprite[2] + sv}
            c1 = Color(self._cur_alpha * self.a, self.r, self.g, self.b)
            local A, R, G, B = c2:ARGB()
            c2 = Color(A * self._cur_alpha, R, G, B)
            rot = self.rot
            draw.texCircle(tex, blend, c1, source, x, y, r, rw, n, m, rot, c2)
        end)
end

lib.defaultFrame = function(self)
    task.Do(self)
    if _boss.is_sc and _boss.timer == 0 then
        self.timer = 0
        self.rot = 0
    end
end

lib.renderFunc = function(self)
    SetViewMode("world")
    local showboss = lstg.tmpvar.bg and lstg.tmpvar.bg.hide == true
    if showboss then
        background.WarpEffectCapture()
    end
    local c = self.fogColor or lstg.view3d.fog[3]
    local a, r, g, b = c:ARGB()
    SetImageState("white", "", Color(a * self.alpha, r, g, b))
    RenderRect("white", lstg.world.l, lstg.world.r, lstg.world.b, lstg.world.t)
    SetImageState("white", "", Color(0xFFFFFFFF))
    if self.layers and type(self.layers) == "table" then
        for i = 1, #(self.layers) do
            local l = self.layers[i]
            l.render(l)
        end
    end
    if showboss then
        background.WarpEffectApply()
    end
end

return lib