local lib = {}

lib.CreateTexture = function(tex, mipmap)
    local w, h = GetTextureSize(tex)
    CreateRenderTarget(tex .. "_mirror", w * 2, h * 2, mipmap or false)
    SetTextureSamplerState(tex .. "_mirror", "linear+wrap")
    return tex .. "_mirror"
end

local function mirrorTexViewMode(tex)
    local function setViewportAndScissorRect(l, r, b, t)
        SetViewport(l, r, b, t)
        SetScissorRect(l, r, b, t)
    end
    local w, h = GetTextureSize(tex)
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

lib.CaptureTexture = function(tex)
    local w, h = GetTextureSize(tex)
    local s = {
        {-1, 0, 0, 1}, {0, 1, 0, 1},
        {-1, 0, 0, -1}, {0, 1, 0, -1},
    }
    local c = Color(0xFFFFFFFF)
    PushRenderTarget(tex .. "_mirror")
    RenderClear(Color(0x00000000))
    mirrorTexViewMode()
    local x, y = w, h
    for i = 1, 4 do
        local dest = s[i]
        local vertex = {
            {x + w * dest[1], y + h * dest[4], 0.5, 0, 0, c},
            {x + w * dest[2], y + h * dest[4], 0.5, w, 0, c},
            {x + w * dest[2], y + h * dest[3], 0.5, w, h, c},
            {x + w * dest[1], y + h * dest[3], 0.5, 0, h, c},
        }
        RenderTexture(tex, "", vertex[1], vertex[2], vertex[3], vertex[4])
    end
    PopRenderTarget()
    SetViewMode("world")
end

return lib