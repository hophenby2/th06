local calc = require("liu_10_mc.script.liu_10_mc_math")
-------------------------------------------------------
local lib = {}

---设置视口矩形
local function SetViewRect(l, r, b, t)
    SetViewport(l, r, b, t)
    SetScissorRect(l, r, b, t)
end

---设置视图模式为billboard(用于原作3D魔法阵、枫叶等独立于3D背景之外的物体)<br>
---<b>fov填角度</b>
lib.viewModeBillboard = function(fov)
    local world = lstg.world
    local aspect = (world.r - world.l) / (world.t - world.b)
    local distance = (0.5) / math.tan(fov / 2)
    local s, dx, dy = screen.scale, screen.dx, screen.dy
    fov = math.rad(fov)
    SetViewRect(world.scrl * s + dx, world.scrr * s + dx, world.scrb * s + dy, world.scrt * s + dy)
    SetPerspective(
        0, 0, -distance,
        0, 0, 0,
        0, 1, 0,
        fov, aspect,
        0.001, 5
    )
    SetFog()
    SetImageScale(1)
end

---获取world坐标到billboard坐标的转换矩阵
lib.WorldToBillboard = function(x, y)
    return x / (lstg.world.t - lstg.world.b), y / (lstg.world.t - lstg.world.b)
end

---获取window坐标到billboard坐标的转换矩阵
lib.WindowToBillboard = function(x, y)
    local height = screen.height * screen.scale
    return x / height, y / height
end

---设置视图模式整个窗口(3D)
lib.viewModeWindow3D = function(fov)
    local aspect = (screen.width * screen.scale) / (screen.height * screen.scale)
    local distance = (0.5) * calc.cot(fov / 2)
    fov = math.rad(fov)
    SetViewRect(0, screen.width * screen.scale, 0, screen.height * screen.scale)
    SetPerspective(
        0, 0, -distance,
        0, 0, 0,
        0, 1, 0,
        fov, aspect,
        0.001, 5
    )
    SetFog()
end

---@alias draw3D_billboard nil|"world"|"window"

---@texture 绘制纹理

---绘制纹理到2D矩形上<br>
---left right bottom top<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param dest table 目标矩形
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param color lstg.Color 颜色
---@param angle number 旋转角度
lib.Rect2D = function(name, blend, color, dest, source, x, y, angle)
    angle = angle or 0
    local x0, y0 = calc.Rotate2D(dest[1], dest[4], angle)
    local x1, y1 = calc.Rotate2D(dest[2], dest[4], angle)
    local x2, y2 = calc.Rotate2D(dest[2], dest[3], angle)
    local x3, y3 = calc.Rotate2D(dest[1], dest[3], angle)
    RenderTexture(name, blend,
    {x + x0, y + y0, 0.5, source[1], source[4], color},
    {x + x1, y + y1, 0.5, source[2], source[4], color},
    {x + x2, y + y2, 0.5, source[2], source[3], color},
    {x + x3, y + y3, 0.5, source[1], source[3], color})
end

---绘制纹理到2D矩形上(渐变)<br>
---left right bottom top<br>
---渐变方向为从左到右<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param color2 lstg.Color 颜色2
---@param dest table 目标矩形
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param angle number 旋转角度
lib.RectGrad2D = function(name, blend, color1, color2, dest, source, x, y, angle)
    angle = angle or 0
    local x0, y0 = calc.Rotate2D(dest[1], dest[4], angle)
    local x1, y1 = calc.Rotate2D(dest[2], dest[4], angle)
    local x2, y2 = calc.Rotate2D(dest[2], dest[3], angle)
    local x3, y3 = calc.Rotate2D(dest[1], dest[3], angle)
    RenderTexture(name, blend,
    {x + x0, y + y0, 0.5, source[1], source[4], color1},
    {x + x1, y + y1, 0.5, source[2], source[4], color2},
    {x + x2, y + y2, 0.5, source[2], source[3], color2},
    {x + x3, y + y3, 0.5, source[1], source[3], color1})
end

---绘制纹理到3D矩形上<br>
---left right bottom top<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param color lstg.Color 颜色
---@param dest table 目标矩形
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param z number 绘制位置z
---@param angleX number 旋转角度X
---@param angleY number 旋转角度Y
---@param angleZ number 旋转角度Z
---@param billboard draw3D_billboard billboard坐标转换
lib.Rect3D = function(name, blend, color, dest, source, x, y, z, angleX, angleY, angleZ, billboard)
    if billboard == "world" then
        dest[1], dest[3] = lib.WorldToBillboard(dest[1], dest[3])
        dest[2], dest[4] = lib.WorldToBillboard(dest[2], dest[4])
    elseif billboard == "window" then
        dest[1], dest[3] = lib.WindowToBillboard(dest[1], dest[3])
        dest[2], dest[4] = lib.WindowToBillboard(dest[2], dest[4])
    end
    local x0, y0, z0 = calc.Rotate3D(dest[1], dest[4], 0, angleX, angleY, angleZ)
    local x1, y1, z1 = calc.Rotate3D(dest[2], dest[4], 0, angleX, angleY, angleZ)
    local x2, y2, z2 = calc.Rotate3D(dest[2], dest[3], 0, angleX, angleY, angleZ)
    local x3, y3, z3 = calc.Rotate3D(dest[1], dest[3], 0, angleX, angleY, angleZ)
    RenderTexture(name, blend,
    {x + x0, y + y0, z + z0, source[1], source[4], color},
    {x + x1, y + y1, z + z1, source[2], source[4], color},
    {x + x2, y + y2, z + z2, source[2], source[3], color},
    {x + x3, y + y3, z + z3, source[1], source[3], color})
end

---绘制纹理到3D矩形上(渐变)<br>
---left right bottom top<br>
---渐变方向为从左到右<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param color2 lstg.Color 颜色2
---@param dest table 目标矩形
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param z number 绘制位置z
---@param angleX number 旋转角度X
---@param angleY number 旋转角度Y
---@param angleZ number 旋转角度Z
---@param billboard draw3D_billboard billboard坐标转换
lib.RectGrad3D = function(name, blend, color1, color2, dest, source, x, y, z, angleX, angleY, angleZ, billboard)
    if billboard == "world" then
        dest[1], dest[3] = lib.WorldToBillboard(dest[1], dest[3])
        dest[2], dest[4] = lib.WorldToBillboard(dest[2], dest[4])
    elseif billboard == "window" then
        dest[1], dest[3] = lib.WindowToBillboard(dest[1], dest[3])
        dest[2], dest[4] = lib.WindowToBillboard(dest[2], dest[4])
    end
    local x0, y0, z0 = calc.Rotate3D(dest[1], dest[4], 0, angleX, angleY, angleZ)
    local x1, y1, z1 = calc.Rotate3D(dest[2], dest[4], 0, angleX, angleY, angleZ)
    local x2, y2, z2 = calc.Rotate3D(dest[2], dest[3], 0, angleX, angleY, angleZ)
    local x3, y3, z3 = calc.Rotate3D(dest[1], dest[3], 0, angleX, angleY, angleZ)
    RenderTexture(name, blend,
    {x + x0, y + y0, z + z0, source[1], source[4], color1},
    {x + x1, y + y1, z + z1, source[2], source[4], color2},
    {x + x2, y + y2, z + z2, source[2], source[3], color2},
    {x + x3, y + y3, z + z3, source[1], source[3], color1})
end

---@sprite  绘制精灵

---绘制精灵到2D矩形上<br>
---left right bottom top<br>
---@param name string 精灵名
---@param blend lstg.BlendMode 混合模式
---@param color lstg.Color 颜色
---@param dest table 目标矩形
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param angle number 旋转角度
lib.RectSprite2D = function(name, blend, color, dest, source, x, y, angle)
    angle = angle or 0
    local x0, y0 = calc.Rotate2D(dest[1], dest[4], angle)
    local x1, y1 = calc.Rotate2D(dest[2], dest[4], angle)
    local x2, y2 = calc.Rotate2D(dest[2], dest[3], angle)
    local x3, y3 = calc.Rotate2D(dest[1], dest[3], angle)
    SetImageState(name, blend, color)
    Render4V(name,
    x + x0, y + y0, 0.5,
    x + x1, y + y1, 0.5,
    x + x2, y + y2, 0.5,
    x + x3, y + y3, 0.5)
    SetImageState(name, "", Color(0xFFFFFFFF))
end

---绘制精灵到2D矩形上(渐变)<br>
---left right bottom top<br>
---渐变方向为从左到右<br>
---@param name string 精灵名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param color2 lstg.Color 颜色2
---@param dest table 目标矩形
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param angle number 旋转角度
lib.RectGradSprite2D = function(name, blend, color1, color2, dest, source, x, y, angle)
    angle = angle or 0
    local x0, y0 = calc.Rotate2D(dest[1], dest[4], angle)
    local x1, y1 = calc.Rotate2D(dest[2], dest[4], angle)
    local x2, y2 = calc.Rotate2D(dest[2], dest[3], angle)
    local x3, y3 = calc.Rotate2D(dest[1], dest[3], angle)
    SetImageState(name, blend, color1, color2)
    Render4V(name,
    x + x0, y + y0, 0.5,
    x + x1, y + y1, 0.5,
    x + x2, y + y2, 0.5,
    x + x3, y + y3, 0.5)
    SetImageState(name, "", Color(0xFFFFFFFF))
end

---绘制精灵到3D矩形上<br>
---left right bottom top<br>
---@param name string 精灵名
---@param blend lstg.BlendMode 混合模式
---@param color lstg.Color 颜色
---@param dest table 目标矩形
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param z number 绘制位置z
---@param angleX number 旋转角度X
---@param angleY number 旋转角度Y
---@param angleZ number 旋转角度Z
---@param billboard draw3D_billboard billboard坐标转换
lib.RectSprite3D = function(name, blend, color, dest, source, x, y, z, angleX, angleY, angleZ, billboard)
    if billboard == "world" then
        dest[1], dest[3] = lib.WorldToBillboard(dest[1], dest[3])
        dest[2], dest[4] = lib.WorldToBillboard(dest[2], dest[4])
    elseif billboard == "window" then
        dest[1], dest[3] = lib.WindowToBillboard(dest[1], dest[3])
        dest[2], dest[4] = lib.WindowToBillboard(dest[2], dest[4])
    end
    local x0, y0, z0 = calc.Rotate3D(dest[1], dest[4], 0, angleX, angleY, angleZ)
    local x1, y1, z1 = calc.Rotate3D(dest[2], dest[4], 0, angleX, angleY, angleZ)
    local x2, y2, z2 = calc.Rotate3D(dest[2], dest[3], 0, angleX, angleY, angleZ)
    local x3, y3, z3 = calc.Rotate3D(dest[1], dest[3], 0, angleX, angleY, angleZ)
    SetImageState(name, blend, color)
    Render4V(name,
    x + x0, y + y0, z + z0,
    x + x1, y + y1, z + z1,
    x + x2, y + y2, z + z2,
    x + x3, y + y3, z + z3)
    SetImageState(name, "", Color(0xFFFFFFFF))
end

---绘制精灵到3D矩形上(渐变)<br>
---left right bottom top<br>
---渐变方向为从左到右<br>
---@param name string 精灵名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param color2 lstg.Color 颜色2
---@param dest table 目标矩形
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param z number 绘制位置z
---@param angleX number 旋转角度X
---@param angleY number 旋转角度Y
---@param angleZ number 旋转角度Z
---@param billboard draw3D_billboard billboard坐标转换
lib.RectGradSprite3D = function(name, blend, color1, color2, dest, source, x, y, z, angleX, angleY, angleZ, billboard)
    if billboard == "world" then
        dest[1], dest[3] = lib.WorldToBillboard(dest[1], dest[3])
        dest[2], dest[4] = lib.WorldToBillboard(dest[2], dest[4])
    elseif billboard == "window" then
        dest[1], dest[3] = lib.WindowToBillboard(dest[1], dest[3])
        dest[2], dest[4] = lib.WindowToBillboard(dest[2], dest[4])
    end
    local x0, y0, z0 = calc.Rotate3D(dest[1], dest[4], 0, angleX, angleY, angleZ)
    local x1, y1, z1 = calc.Rotate3D(dest[2], dest[4], 0, angleX, angleY, angleZ)
    local x2, y2, z2 = calc.Rotate3D(dest[2], dest[3], 0, angleX, angleY, angleZ)
    local x3, y3, z3 = calc.Rotate3D(dest[1], dest[3], 0, angleX, angleY, angleZ)
    SetImageState(name, blend, color1, color2)
    Render4V(name,
    x + x0, y + y0, z + z0,
    x + x1, y + y1, z + z1,
    x + x2, y + y2, z + z2,
    x + x3, y + y3, z + z3)
    SetImageState(name, "", Color(0xFFFFFFFF))
end

---@anm thANM的绘制函数

---绘制纹理到2D环形上<br>
---nmax为边数<br>
---以angle为起始角度点，顺时针方向绘制<br>
---dest[3]必须大于dest[4]<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param radius number 环的半径
---@param scale number 环的宽度
---@param nmax number 边数
---@param re number 纹理重复次数
---@param angle number 起始角度
---@param color2 lstg.Color|nil 颜色2(nil表示与颜色1相同)
lib.texCircle = function(name, blend, color1, source, x, y, radius, scale, nmax, re, angle, color2)
    color2 = color2 or color1
    angle = angle or 0
    local r0, r1 = radius + abs(scale / 2), radius - abs(scale / 2)
    local a, da = angle, 360 / nmax
    local h = (source[3] - source[4]) * re
    for i = 0, (nmax - 1) do
        local x0, y0 = r0 * cos(a - 0), r0 * sin(a - 0)
        local x1, y1 = r0 * cos(a - da), r0 * sin(a - da)
        local x2, y2 = r1 * cos(a - da), r1 * sin(a - da)
        local x3, y3 = r1 * cos(a - 0), r1 * sin(a - 0)
        RenderTexture(name, blend,
        {x + x0, y + y0, 0.5, source[1], source[4] + h / nmax * i, color1},
        {x + x1, y + y1, 0.5, source[1], source[4] + h / nmax * (i + 1), color1},
        {x + x2, y + y2, 0.5, source[2], source[4] + h / nmax * (i + 1), color2},
        {x + x3, y + y3, 0.5, source[2], source[4] + h / nmax * i, color2})
        a = a - da
    end
end

---绘制纹理到2D弧形上<br>
---nmax为边数<br>
---以角度angle为中心，顺时针方向绘制
---dest[3]必须大于dest[4]<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param radius number 环的半径
---@param scale number 环的宽度
---@param nmax number 边数
---@param re number 纹理重复次数
---@param Oangle number 扇形角度
---@param angle number 中心角度
---@param color2 lstg.Color|nil 颜色2(nil表示与颜色1相同)
lib.texArcEven = function(name, blend, color1, source, x, y, radius, scale, nmax, re, Oangle, angle, color2)
    color2 = color2 or color1
    angle = angle or 0
    local r0, r1 = radius + abs(scale / 2), radius - abs(scale / 2)
    local a, da = angle + abs(Oangle) / 2, Oangle / nmax
    local h = (source[3] - source[4]) * re
    for i = 0, (nmax - 1) do
        local x0, y0 = r0 * cos(a - 0), r0 * sin(a - 0)
        local x1, y1 = r0 * cos(a - da), r0 * sin(a - da)
        local x2, y2 = r1 * cos(a - da), r1 * sin(a - da)
        local x3, y3 = r1 * cos(a - 0), r1 * sin(a - 0)
        RenderTexture(name, blend,
        {x + x0, y + y0, 0.5, source[1], source[4] + h / nmax * i, color1},
        {x + x1, y + y1, 0.5, source[1], source[4] + h / nmax * (i + 1), color1},
        {x + x2, y + y2, 0.5, source[2], source[4] + h / nmax * (i + 1), color2},
        {x + x3, y + y3, 0.5, source[2], source[4] + h / nmax * i, color2})
        a = a - da
    end
end

---绘制纹理到2D弧形上<br>
---nmax为边数<br>
---以角度angle为起点，顺时针方向绘制
---dest[3]必须大于dest[4]<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param radius number 环的半径
---@param scale number 环的宽度
---@param nmax number 边数
---@param re number 纹理重复次数
---@param Oangle number 扇形角度
---@param angle number 起始角度
---@param color2 lstg.Color|nil 颜色2(nil表示与颜色1相同)
lib.texArc = function(name, blend, color1, source, x, y, radius, scale, nmax, re, Oangle, angle, color2)
    color2 = color2 or color1
    angle = angle or 0
    local r0, r1 = radius + abs(scale / 2), radius - abs(scale / 2)
    local a, da = angle, abs(Oangle) / nmax
    local h = (source[3] - source[4]) * re
    for i = 0, (nmax - 1) do
        local x0, y0 = r0 * cos(a - 0), r0 * sin(a - 0)
        local x1, y1 = r0 * cos(a - da), r0 * sin(a - da)
        local x2, y2 = r1 * cos(a - da), r1 * sin(a - da)
        local x3, y3 = r1 * cos(a - 0), r1 * sin(a - 0)
        RenderTexture(name, blend,
        {x + x0, y + y0, 0.5, source[1], source[4] + h / nmax * i, color1},
        {x + x1, y + y1, 0.5, source[1], source[4] + h / nmax * (i + 1), color1},
        {x + x2, y + y2, 0.5, source[2], source[4] + h / nmax * (i + 1), color2},
        {x + x3, y + y3, 0.5, source[2], source[4] + h / nmax * i, color2})
        a = a - da
    end
end

---绘制具有给定尺寸的填充矩形<br>
---@param blend lstg.BlendMode 混合模式
---@param color lstg.Color 颜色
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param w number 矩形宽度
---@param h number 矩形高度
---@param angle number 旋转角度
lib.drawRect = function(blend, color, x, y, w, h, angle)
    angle = angle or 0
    local x0, y0 = calc.Rotate2D(-w / 2, h / 2, angle)
    local x1, y1 = calc.Rotate2D(w / 2, h / 2, angle)
    local x2, y2 = calc.Rotate2D(w / 2, -h / 2, angle)
    local x3, y3 = calc.Rotate2D(-w / 2, -h / 2, angle)
    SetImageState("white", blend, color)
    Render4V("white",
    x + x0, y + y0, 0.5,
    x + x1, y + y1, 0.5,
    x + x2, y + y2, 0.5,
    x + x3, y + y3, 0.5)
    SetImageState("white", "", Color(0xFFFFFFFF))
end

---绘制填充的规则n边形<br>
---nmax为边数<br>
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param radius number 半径
---@param nmax number 边数
---@param angle number 旋转角度
---@param color2 lstg.Color|nil 颜色2(nil表示与颜色1相同)
lib.drawPoly = function(blend, color1, x, y, radius, nmax, angle, color2)
    color2 = color2 or color1
    angle = angle or 0
    local a, da = angle, 360 / nmax
    local r0, r1 = 0, radius
    SetImageState("white", blend, color1, color1, color2, color2)
    for i = 0, (nmax - 1) do
        local x0, y0 = r0 * cos(a - 0), r0 * sin(a - 0)
        local x1, y1 = r0 * cos(a - da), r0 * sin(a - da)
        local x2, y2 = r1 * cos(a - da), r1 * sin(a - da)
        local x3, y3 = r1 * cos(a - 0), r1 * sin(a - 0)
        Render4V("white",
        x + x0, y + y0, 0.5,
        x + x1, y + y1, 0.5,
        x + x2, y + y2, 0.5,
        x + x3, y + y3, 0.5)
        a = a - da
    end
    SetImageState("white", "", Color(0xFFFFFFFF))
end

---与drawPoly类似，但只绘制1像素的边框(无渐变)<br>
---nmax为边数<br>
---@param blend lstg.BlendMode 混合模式
---@param color lstg.Color 颜色
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param radius number 半径
---@param nmax number 边数
---@param angle number 旋转角度
lib.drawPolyBorder = function(blend, color, x, y, radius, nmax, angle)
    angle = angle or 0
    local a, da = angle, 360 / nmax
    local r0, r1 = radius - 1, radius
    SetImageState("white", blend, color)
    for i = 0, (nmax - 1) do
        local x0, y0 = r0 * cos(a - 0), r0 * sin(a - 0)
        local x1, y1 = r0 * cos(a - da), r0 * sin(a - da)
        local x2, y2 = r1 * cos(a - da), r1 * sin(a - da)
        local x3, y3 = r1 * cos(a - 0), r1 * sin(a - 0)
        Render4V("white",
        x + x0, y + y0, 0.5,
        x + x1, y + y1, 0.5,
        x + x2, y + y2, 0.5,
        x + x3, y + y3, 0.5)
        a = a - da
    end
    SetImageState("white", "", Color(0xFFFFFFFF))
end

---与drawRect相同,但支持从左往右的渐变<br>
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param w number 矩形宽度
---@param h number 矩形高度
---@param angle number 旋转角度
---@param color2 lstg.Color|nil 颜色2(nil表示与颜色1相同)
lib.drawRectGrad = function(blend, color1, x, y, w, h, angle, color2)
    color2 = color2 or color1
    angle = angle or 0
    local x0, y0 = calc.Rotate2D(-w / 2, h / 2, angle)
    local x1, y1 = calc.Rotate2D(w / 2, h / 2, angle)
    local x2, y2 = calc.Rotate2D(w / 2, -h / 2, angle)
    local x3, y3 = calc.Rotate2D(-w / 2, -h / 2, angle)
    SetImageState("white", blend, color1, color2, color2, color1)
    Render4V("white",
    x + x0, y + y0, 0.5,
    x + x1, y + y1, 0.5,
    x + x2, y + y2, 0.5,
    x + x3, y + y3, 0.5)
    SetImageState("white", "", Color(0xFFFFFFFF))
end

---绘制纹理绘制纹理到3D曲面上(圆柱体截面)<br>
---nmax为边数<br>
---以角度angle为中心，顺时针方向绘制
---dest[3]必须大于dest[4]<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param z number 绘制位置z
---@param radius number 半径
---@param height number 高度
---@param nmax number 边数
---@param re number 纹理重复次数
---@param angleX number 旋转角度X
---@param angleY number 旋转角度Y
---@param angleZ number 旋转角度Z
---@param Oangle number 扇形角度
---@param angle number 起始角度
---@param billboard draw3D_billboard billboard模式
---@param color2 lstg.Color|nil 颜色2(nil表示与颜色1相同)
lib.texCylinder3D = function(name, blend, color1, source, x, y, z, radius, height, nmax, re, angleX, angleY, angleZ, Oangle, angle, billboard, color2)
    color2 = color2 or color1
    if billboard == "world" then
        radius, height = lib.WorldToBillboard(radius, height)
    elseif billboard == "window" then
        radius, height = lib.WindowToBillboard(radius, height)
    end
    local h0, h1 = height / 2, -height / 2
    local a, da = angle + abs(Oangle) / 2, abs(Oangle) / nmax
    local h = (source[3] - source[4]) * re
    for i = 0, (nmax - 1) do
        local x0, y0, z0 = calc.Rotate3D(radius * cos(a - 0), radius * sin(a - 0), h0, angleX, angleY, angleZ)
        local x1, y1, z1 = calc.Rotate3D(radius * cos(a - da), radius * sin(a - da), h0, angleX, angleY, angleZ)
        local x2, y2, z2 = calc.Rotate3D(radius * cos(a - da), radius * sin(a - da), h1, angleX, angleY, angleZ)
        local x3, y3, z3 = calc.Rotate3D(radius * cos(a - 0), radius * sin(a - 0), h1, angleX, angleY, angleZ)
        RenderTexture(name, blend,
        {x + x0, y + y0, z + z0, source[1], source[4] + h / nmax * i, color1},
        {x + x1, y + y1, z + z1, source[1], source[4] + h / nmax * (i + 1), color1},
        {x + x2, y + y2, z + z2, source[2], source[4] + h / nmax * (i + 1), color2},
        {x + x3, y + y3, z + z3, source[2], source[4] + h / nmax * i, color2})
        a = a - da
    end
end

---绘制纹理到3D环形上(圆环)<br>
---nmax为边数<br>
---以角度angle为中心，顺时针方向绘制<br>
---dest[3]必须大于dest[4]<br>
---@param name string 纹理名
---@param blend lstg.BlendMode 混合模式
---@param color1 lstg.Color 颜色1
---@param source table uv矩形
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param z number 绘制位置z
---@param radius number 半径
---@param scale number 环的宽度
---@param nmax number 边数
---@param re number 纹理重复次数
---@param angleX number 旋转角度X
---@param angleY number 旋转角度Y
---@param angleZ number 旋转角度Z
---@param Oangle number 扇形角度
---@param angle number 起始角度
---@param billboard draw3D_billboard billboard模式
---@param color2 lstg.Color|nil 颜色2(nil表示与颜色1相同)
lib.texRing3D = function(name, blend, color1, source, x, y, z, radius, scale, nmax, re, angleX, angleY, angleZ, Oangle, angle, billboard, color2)
    color2 = color2 or color1
    if billboard == "world" then
        radius, scale = lib.WorldToBillboard(radius, scale)
    elseif billboard == "window" then
        radius, scale = lib.WindowToBillboard(radius, scale)
    end
    local r0, r1 = radius - abs(scale / 2), radius + abs(scale / 2)
    local a, da = angle + abs(Oangle) / 2, abs(Oangle) / nmax
    local h = (source[3] - source[4]) * re
    for i = 0, (nmax - 1) do
        local x0, y0, z0 = calc.Rotate3D(r0 * cos(a - 0), r0 * sin(a - 0), 0, angleX, angleY, angleZ)
        local x1, y1, z1 = calc.Rotate3D(r0 * cos(a - da), r0 * sin(a - da), 0, angleX, angleY, angleZ)
        local x2, y2, z2 = calc.Rotate3D(r1 * cos(a - da), r1 * sin(a - da), 0, angleX, angleY, angleZ)
        local x3, y3, z3 = calc.Rotate3D(r1 * cos(a - 0), r1 * sin(a - 0), 0, angleX, angleY, angleZ)
        RenderTexture(name, blend,
        {x + x0, y + y0, z + z0, source[1], source[4] + h / nmax * i, color1},
        {x + x1, y + y1, z + z1, source[1], source[4] + h / nmax * (i + 1), color1},
        {x + x2, y + y2, z + z2, source[2], source[4] + h / nmax * (i + 1), color2},
        {x + x3, y + y3, z + z3, source[2], source[4] + h / nmax * i, color2})
        a = a - da
    end
end

---绘制一个具有n个边的填充环(环形，无渐变)<br>
---nmax为边数<br>
---@param blend lstg.BlendMode 混合模式
---@param color lstg.Color 颜色
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param radius number 半径
---@param scale number 环的宽度
---@param nmax number 边数
---@param angle number 旋转角度
lib.drawRing = function(blend, color, x, y, radius, scale, nmax, angle)
    angle = angle or 0
    local a, da = angle, 360 / nmax
    local r0, r1 = radius - abs(scale / 2), radius + abs(scale / 2)
    SetImageState("white", blend, color)
    for i = 0, (nmax - 1) do
        local x0, y0 = r0 * cos(a - 0), r0 * sin(a - 0)
        local x1, y1 = r0 * cos(a - da), r0 * sin(a - da)
        local x2, y2 = r1 * cos(a - da), r1 * sin(a - da)
        local x3, y3 = r1 * cos(a - 0), r1 * sin(a - 0)
        Render4V("white",    
        x + x0, y + y0, 0.5,
        x + x1, y + y1, 0.5,
        x + x2, y + y2, 0.5,
        x + x3, y + y3, 0.5)
        a = a - da
    end
    SetImageState("white", "", Color(0xFFFFFFFF))
end

---绘制一个1像素厚的矩形边框<br>
---w为矩形宽度<br>
---h为矩形高度<br>
---angle为旋转角度<br>
---@param blend lstg.BlendMode 混合模式
---@param color lstg.Color 颜色
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param w number 矩形宽度
---@param h number 矩形高度
---@param angle number 旋转角度
lib.drawRectBorder = function(blend, color, x, y, w, h, angle)
    local b1 = {-w / 2, w / 2, -h / 2, h / 2}
    local b2 = {(-w / 2) + 1, (w / 2) - 1, (-h / 2) + 1, (h / 2) - 1}
    local border = {
        {{b1[1], b1[4]}, {b1[2], b1[4]}, {b2[2], b2[4]}, {b2[1], b2[4]}},
        {{b2[2], b2[4]}, {b1[2], b1[4]}, {b1[2], b1[3]}, {b2[2], b2[3]}},
        {{b2[1], b2[3]}, {b2[2], b2[3]}, {b1[2], b1[3]}, {b1[1], b1[3]}},
        {{b1[1], b1[4]}, {b2[1], b2[4]}, {b2[1], b2[3]}, {b1[1], b1[3]}},
    }
    SetImageState("white", blend, color)
    for i = 1, 4 do
        local x0, y0 = calc.Rotate2D(border[i][1][1], border[i][1][2], angle)
        local x1, y1 = calc.Rotate2D(border[i][2][1], border[i][2][2], angle)
        local x2, y2 = calc.Rotate2D(border[i][3][1], border[i][3][2], angle)
        local x3, y3 = calc.Rotate2D(border[i][4][1], border[i][4][2], angle)
        Render4V("white",
        x + x0, y + y0, 0.5,
        x + x1, y + y1, 0.5,
        x + x2, y + y2, 0.5,
        x + x3, y + y3, 0.5)
    end
    SetImageState("white", "", Color(0xFFFFFFFF))
end

---绘制一条1像素粗的水平线<br>
---len为线的长度<br>
---angle为旋转角度<br>
---@param blend lstg.BlendMode 混合模式
---@param color lstg.Color 颜色
---@param x number 绘制位置x
---@param y number 绘制位置y
---@param len number 线的长度
---@param angle number 旋转角度
lib.drawLine = function(blend, color, x, y, len, angle)
    angle = angle or 0
    local w, h = len, 1
    local x0, y0 = calc.Rotate2D(-w / 2, h / 2, angle)
    local x1, y1 = calc.Rotate2D(w / 2, h / 2, angle)
    local x2, y2 = calc.Rotate2D(w / 2, -h / 2, angle)
    local x3, y3 = calc.Rotate2D(-w / 2, -h / 2, angle)
    SetImageState("white", blend, color)
    Render4V("white",
    x + x0, y + y0, 0.5,
    x + x1, y + y1, 0.5,
    x + x2, y + y2, 0.5,
    x + x3, y + y3, 0.5)
    SetImageState("white", "", Color(0xFFFFFFFF))
end

return lib