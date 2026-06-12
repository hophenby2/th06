local lib = {}
--- @type function[]
local Mode = {}

--- 添加模式<br>
--- @param f function 模式函数
--- @param pos number 位置，默认为nil，表示添加到末尾
--- @return function 模式函数
--- @overload fun(f: function): function
local function addMode(f, pos)
    if pos then
        table.insert(Mode, pos, f)
    else
        table.insert(Mode, f)
    end
    return f
end

--- 翻转函数<br>
--- @param f function 原函数
--- @param x number 输入值
--- @return number 输出值
local function flip(f, x)
    return 1 - f(1 - x)
end

--- 分割函数<br>
--- @param f function 起始函数
--- @param g function 终止函数
--- @param x number 输入值
--- @return number 输出值
local function split(f, g, x)
    return x < 0.5 and 0.5 * f(2 * x) or 0.5 * (1 + g(2 * x - 1))
end

--- @===================Zun式插值函数===================
lib.lerp_func = {}
local lerp_func = lib.lerp_func

--- 线性插值函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.linear = addMode(function(x)
    return x
end, 0)

--- easeInQuad 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeIn2 = addMode(function(x)
    return math.pow(x, 2)
end)

--- easeInCubic 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeIn3 = addMode(function(x)
    return math.pow(x, 3)
end)

--- easeInQuart 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeIn4 = addMode(function(x)
    return math.pow(x, 4)
end)

--- easeOutQuad 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOut2 = addMode(function(x)
    return flip(lerp_func.easeIn2, x)
end)

--- easeOutCubic 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOut3 = addMode(function(x)
    return flip(lerp_func.easeIn3, x)
end)

--- easeOutQuart 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOut4 = addMode(function(x)
    return flip(lerp_func.easeIn4, x)
end)

--- 恒定速度
lerp_func.constantVelocity = addMode(function(x)
end)

--- 平滑步骤(严格来说是贝塞尔曲线插值)<br>
--- @param x number 输入值
--- @param y1 number 起始值
--- @param y2 number 终止值
--- @param p1 number 控制点1
--- @param p2 number 控制点2
--- @return number 输出值
lerp_func.smoothStep = addMode(function(x, y1, y2, p1, p2)
    if not y1 then y1 = 0 end
    if not y2 then y2 = 1 end
    if not p1 then p1 = 0 end
    if not p2 then p2 = 1 end
    local x2 = math.pow(x, 2)
    local ix = 1 - x
    local ix2 = math.pow(ix, 2)
    return p1 * x * ix2 - p2 * x2 * ix + y2 * x2 * (3 - x * x) + y1 * ix2 * (2 * x + 1)
end)

--- easeInOutQuad 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInOut2 = addMode(function(x)
    return split(lerp_func.easeIn2, lerp_func.easeOut2, x)
end)

--- easeInOutCubic 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInOut3 = addMode(function(x)
    return split(lerp_func.easeIn3, lerp_func.easeOut3, x)
end)

--- easeInOutQuart 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInOut4 = addMode(function(x)
    return split(lerp_func.easeIn4, lerp_func.easeOut4, x)
end)

--- easeOutInQuad 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutIn2 = addMode(function(x)
    return split(lerp_func.easeOut2, lerp_func.easeIn2, x)
end)

--- easeOutInCubic 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutIn3 = addMode(function(x)
    return split(lerp_func.easeOut3, lerp_func.easeIn3, x)
end)

--- easeOutInQuart 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutIn4 = addMode(function(x)
    return split(lerp_func.easeOut4, lerp_func.easeIn4, x)
end)

--- 延迟变化<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.delayed = addMode(function(x)
    return x == 1 and 1 or 0
end)

--- 立即变化<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.instant = addMode(function(x)
    return flip(lerp_func.delayed, x)
end)

--- 恒定加速度<br>
lerp_func.constantAcceleration = addMode(function(x)
end)

--- easeOutSine 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutSine = addMode(function(x)
    return math.sin(x * math.pi / 2)
end)

--- easeInSine 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInSine = addMode(function(x)
    return flip(lerp_func.easeOutSine, x)
end)

--- easeOutInSine 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutInSine = addMode(function(x)
    return split(lerp_func.easeOutSine, lerp_func.easeInSine, x)
end)

--- easeInOutSine 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInOutSine = addMode(function(x)
    return split(lerp_func.easeInSine, lerp_func.easeOutSine, x)
end)

--- easeInBackA 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInBackA = addMode(function(x)
    return ((math.pow(x - 0.25, 2) / 0.5625) - 0.111111) / 0.888889
end)

--- easeInBackB 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInBackB = addMode(function(x)
    return ((math.pow(x - 0.3, 2) / 0.49) - 0.183673) / 0.816326
end)

--- easeInBackC 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInBackC = addMode(function(x)
    return ((math.pow(x - 0.35, 2) / 0.4225) - 0.289941) / 0.710059
end)

--- easeInBackD 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInBackD = addMode(function(x)
    return ((math.pow(x - 0.38, 2) / 0.3844) - 0.37565) / 0.62435
end)

--- easeInBackE 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeInBackE = addMode(function(x)
    return ((math.pow(x - 0.4, 2) / 0.36) - 0.444444) / 0.555556
end)

--- easeOutBackA 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutBackA = addMode(function(x)
    return flip(lerp_func.easeInBackA, x)
end)

--- easeOutBackB 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutBackB = addMode(function(x)
    return flip(lerp_func.easeInBackB, x)
end)

--- easeOutBackC 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutBackC = addMode(function(x)
    return flip(lerp_func.easeInBackC, x)
end)

--- easeOutBackD 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutBackD = addMode(function(x)
    return flip(lerp_func.easeInBackD, x)
end)

--- easeOutBackE 缓动函数<br>
--- @param x number 输入值
--- @return number 输出值
lerp_func.easeOutBackE = addMode(function(x)
    return flip(lerp_func.easeInBackE, x)
end)

--- Zun式插值函数,i取值范围0-1,mode为插值模式,返回插值结果<br>
--- @param from number 起始值
--- @param to number 终止值
--- @param i number 输入值
--- @param mode number|function 插值模式
--- @return number 输出值
lib.lerp = function(from, to, i, mode)
    if mode == 7 or mode == Mode[7] then
        return from + to * i
    elseif mode == 17 or mode == Mode[17] then
        return from + to * math.pow(i, 2)
    else
        if type(mode) == "function" then
            return from + (to - from) * mode(i)
        elseif type(mode) == "number" then
            return from + (to - from) * Mode[mode](i)
        else
            error("Invalid mode")
        end
    end
end

--- 使用于task的插值函数
--- @param tar table 目标对象
--- @param var string | number 目标属性
--- @param value number 目标值
--- @param t number 持续时间
--- @param mode number|function 插值模式
lib.LerpTo = function(tar, var, value, t, mode)
    task.New(task.GetSelf(), function()
        local cache = tar[var]
        for i = 0, t do
            tar[var] = lib.lerp(cache, value, i / t, mode)
            task.Wait(1)
        end
        tar[var] = value
    end)
end

--- 贝塞尔曲线插值<br>
lib.bezier = lerp_func.smoothStep

--- @===================数学系轮子===================

lib.rad = math.rad
lib.deg = math.deg

--- 四舍五入<br>
--- @param x number 输入值
--- @return number 输出值
lib.round = function(x)
    if x >= 0 then
        return math.floor(x + 0.5)
    else
        return math.ceil(x - 0.5)
    end
end

---将x限制在a和b之间<br>
--- @param x number 输入值
--- @param a number 最小值
--- @param b number 最大值
--- @return number 输出值
lib.clamp = function(x, a, b)
    return math.max(a, math.min(b, x))
end

--- 判断x是否在a和b之间<br>
--- @param x number 输入值
--- @param a number 最小值
--- @param b number 最大值
--- @return boolean 输出值
lib.insope = function(x, a, b)
    return x >= a and x <= b
end

--- 返回 1 / tan(x)<br>
--- @param x number 输入值
--- @return number 输出值
lib.cot = function(x)
    return 1 / tan(x)
end

--- 返回 1 / cos(x)<br>
--- @param x number 输入值
--- @return number 输出值
lib.sec = function(x)
    return 1 / cos(x)
end

--- 返回 1 / sin(x)<br>
--- @param x number 输入值
--- @return number 输出值
lib.csc = function(x)
    return 1 / sin(x)
end

--- @弧度制
lib.rcos = math.cos
lib.rsin = math.sin
lib.rtan = math.tan
lib.racos = math.acos
lib.rsacos = math.asin
lib.ratan = math.atan
lib.ratan2 = math.atan2

--- cot的弧度制版本<br>
--- @param x number 输入值
--- @return number 输出值
lib.rcot = function(x)
    return 1 / lib.rtan(x)
end

--- sec的弧度制版本<br>
--- @param x number 输入值
--- @return number 输出值
lib.rsec = function(x)
    return 1 / lib.rcos(x)
end

--- csc的弧度制版本<br>
--- @param x number 输入值
--- @return number 输出值
lib.rcsc = function(x)
    return 1 / lib.rsin(x)
end

--- @===================逆时针角度(弧度)转顺时针角度(弧度)===================

---弧度转角度(顺时针转逆时针)<br>
--- @param x number 输入值
--- @return number 输出值
lib.Deg = function(x)
    return -math.deg(x)
end

---角度转弧度(逆时针转顺时针)<br>
--- @param x number 输入值
--- @return number 输出值
lib.Rad = function(x)
    return -math.rad(x)
end

--- 将角度规范化(-180~180)<br>
--- @param a number 输入值
--- @return number 输出值
lib.normalizeAngle = function(a)
    return (a + 180) % 360 - 180
end

--- normalizeAngle的弧度制版本<br>
--- @param a number 输入值
--- @return number 输出值
lib.normalizeAngleRad = function(a)
    return (a + math.pi) % (math.pi * 2) - math.pi
end

--- 加减+-360使角度a处于(-180~180)之间,但只会循环34次<br>
--- @param a number 输入值
--- @return number 输出值
lib.validDeg = function(a)
    for _ = 1, 34 do
        if a > 180 then
            a = a - 360
        elseif a < -180 then
            a = a + 360
        else break end
    end
    return a
end

--- 加减+-2π使角度a处于(-π~π)之间,但只会循环34次<br>
--- @param a number 输入值
--- @return number 输出值
lib.validDegRad = function(a)
    for _ = 1, 34 do
        if a > math.pi then
            a = a - math.pi * 2
        elseif a < -math.pi then
            a = a + math.pi * 2
        else break end
    end
    return a
end

--- @===================向量与矩阵===================
--- @class matrix
--- 创建一个mxn的矩阵<br>
--- mn是数组{m, n}<br>
--- 推荐直接按格式 {{}, {}, {}, ...}手动创建
lib.CreateMatrix = function(mn, ...)
    local mat = {}
    local index = 1
    local j = 1
    for i = 1, mn[2] do
        mat[i] = {}
    end
    for _, v in ipairs({...}) do
        mat[j][index] = v
        if index >= mn[1] then
            index = 1
            j = j + 1
        else
            index = index + 1
        end
    end
    return mat
end

--- 矩阵相乘<br>
--- 仅支持矩形矩阵<br>
--- @param A table 矩阵1
--- @param B table 矩阵2
--- @return table 矩阵
lib.MatrixMix = function(A, B)
    local A_m, B_m = #A[1], #B[1]
    local B_n = #B
    local mix = {}
    local add = 0
    for j = 1, B_n do
        mix[j] = {}
        for i = 1, B_m do
            for ai = 1, A_m do
                add = add + (B[ai][i] * A[j][ai]) * 1
            end
            mix[j][i] = add
            add = 0
        end
    end
    return mix
end

--- 矩阵乘法<br>
--- @param B table 矩阵
--- @param num number 数值
--- @return table 矩阵
lib.MatrixMultiply = function(B, num)
    local B_m = #B[1]
    local B_n = #B
    local mix = {}
    for j = 1, B_n do
        mix[j] = {}
        for i = 1, B_m do
            mix[j][i] = B[j][i] * num
        end
    end
    return mix
end

--- @class vector3
--- 创建一个三维向量
lib.CreateVector3 = function(x, y, z)
    return {x = x, y = y, z = z}
end

--- 向量相加<br>
--- @param v1 table 向量1
--- @param v2 table 向量2
--- @return table 向量
lib.addVector3 = function(v1, v2)
    local v = {x = v1.x + v2.x, y = v1.y + v2.y, z = v1.z + v2.z}
    return v
end

--- 向量相减<br>
--- @param v1 table 向量1
--- @param v2 table 向量2
--- @return table 向量
lib.minusVector3 = function(v1, v2)
    local v = {x = v1.x - v2.x, y = v1.y - v2.y, z = v1.z - v2.z}
    return v
end

--- 向量点乘(数量积)<br>
--- @param v1 table 向量1
--- @param v2 table 向量2
--- @return table 向量
lib.dotVector3 = function(v1, v2)
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
end

--- 向量叉乘
--- @param v1 table 向量1
--- @param v2 table 向量2
--- @return table 向量
lib.crossVector3 = function(v1, v2)
    local v = {x = v1.y * v2.z - v2.y * v1.z, y = v2.x * v1.z - v1.x * v2.z, z = v1.x * v2.y - v2.x * v1.y}
    return v
end

--- 向量倒数
--- @param v table 向量
--- @return table 向量
lib.Get_1_Vector3 = function(v)
    return {x = 1 / v.x, y = 1 / v.y, z = 1 / v.z}
end

--- 向量归一化
--- @param v table 向量
--- @return table 向量
lib.normalizeVector3 = function(v)
    local d = math.sqrt(math.pow(v.x, 2) + math.pow(v.y, 2) + math.pow(v.z, 2))
    return {x = v.x / d, y = v.y / d, z = v.z / d}
end

--- 向量转齐次矩阵(向量)
--- @param v table 向量
--- @return table 矩阵
lib.Vector3ToMatrix = function(v)
    local mat = {
        {v.x}, {v.y}, {v.z}, {1}
    }
    return mat
end

---向量转齐次矩阵(点)
--- @param v table 向量
--- @return table 矩阵
lib.Vector3ToMatrixPoint = function(v)
    local mat = {
        {v.x}, {v.y}, {v.z}, {0}
    }
    return mat
end

---LookAt矩阵(含平移)
--- @param pos table 位置
--- @param target table 目标
--- @param upDir table 上方向
--- @return table 矩阵
lib.MatLookAt = function(pos, target, upDir)
    local cN = lib.normalizeVector3(lib.minusVector3(target, pos))
    local cU = lib.normalizeVector3(lib.crossVector3(upDir, cN))
    local cV = lib.crossVector3(cN, cU)

    local eU = lib.dotVector3(pos, cU)
    local eV = lib.dotVector3(pos, cV)
    local eN = lib.dotVector3(pos, cN)

    local mat = {
        {cU.x, cU.y, cU.z, -eU},
        {cV.x, cV.y, cV.z, -eV},
        {cN.x, cN.y, cN.z, -eN},
        {0, 0, 0, 1}
    }
    return mat
end

--- 透视除法矩阵(w分量上保留深度信息)<br>
--- 可以根据z分量是否处于(-zn, zf)范围内进行*裁剪*<br>
--- 注意zn必须 >= 0<br>
--- <b>注意此处fov为弧度制</b><br>
--- @param fov number 视角(弧度制)
--- @param aspect number 宽高比
--- @param zn number 近裁剪面
--- @param zf number 远裁剪面
--- @return table 矩阵
lib.MatProjection = function(fov, aspect, zn, zf)
    fov = math.deg(fov * 0.5)
    local e11 = lib.cot(fov) / aspect
    local e22 = lib.cot(fov)
    local e33 = (zf + zn) / (zf - zn)
    local e34 = -(2 * (zf * zn) / (zf - zn))
    local e43 = 1.0
    local proj = {
        {e11, 0, 0, 0},
        {0, e22, 0, 0},
        {0, 0, e33, e34},
        {0, 0, e43, 0}
    }
    return proj
end

--- 创建视口变化矩阵<br>
--- x,y原点坐标(向右下为正方向)
--- @param x number x坐标
--- @param y number y坐标
--- @param width number 视口宽度
--- @param height number 视口高度
--- @param maxZ number 视口最大深度
--- @param minZ number 视口最小深度
--- @return table 矩阵
lib.MatViewport = function(x, y, width, height, maxZ, minZ)
    return {
        {width / 2, 0, 0, x},
        {0, height / 2, 0, y},
        {0, 0, maxZ - minZ, 0},
        {width / 2, height / 2, minZ, 1}
    }
end

--- 3D坐标转屏幕2D坐标<br>
--- 有flag时返回的是裁剪空间下的深度值(做billboard可用)<br>
--- @param lookat table lookat矩阵
--- @param proj table 透视矩阵
--- @param viewport table 视口矩阵
--- @param p table 三维向量xyz
--- @param flag boolean 是否返回深度值
--- @return number x坐标, number y坐标, number z坐标或深度值
lib.From3DToWorld = function(lookat, proj, viewport, p, flag)
    p = lib.Vector3ToMatrix(p)
    p = lib.MatrixMix(lookat, p)
    p = lib.MatrixMix(proj, p)
    local w, z = p[4][1], p[3][1]
    p = lib.MatrixMultiply(p, 1 / w)
    p = lib.MatrixMix(viewport, p)

    if flag then
        return p[1][1], p[2][1], z
    else
        return p[1][1], p[2][1], w
    end
end

--- 二維旋轉(角度制)<br>
--- 绕点(0, 0)旋转a度
--- @param x number x坐标
--- @param y number y坐标
--- @param a number 旋转角(角度制)
--- @return number x坐标, number y坐标
lib.Rotate2D = function(x, y, a)
    return x * cos(a) - y * sin(a), x * sin(a) + y * cos(a)
end

--- 三維旋轉(角度制)<br>
--- 绕点(0, 0, 0)旋转(a,b,c)度
--- @param x number x坐标
--- @param y number y坐标
--- @param z number z坐标
--- @param a number x轴旋转角(角度制)
--- @param b number y轴旋转角(角度制)
--- @param c number z轴旋转角(角度制)
--- @return number x坐标, number y坐标, number z坐标
lib.Rotate3D = function(x, y, z, a, b, c)
    local p = {
        {x}, {y}, {z}
    }
    local XR = {
        {1, 0, 0},
        {0, cos(a), -sin(a)},
        {0, sin(a), cos(a)}
    }
    local YR = {
        {cos(b), 0, -sin(b)},
        {0, 1, 0},
        {sin(b), 0, cos(b)}
    }
    local ZR = {
        {cos(c), sin(c), 0},
        {-sin(c), cos(c), 0},
        {0, 0, 1}
    }
    local temp = lib.MatrixMix(ZR, YR)
    local r = lib.MatrixMix(XR, temp)
    p = lib.MatrixMix(r, p)
    return p[1][1], p[2][1], p[3][1]
end

---@===================随机数===================

lib.rnd = {}

--- 返回一个a~b之间的随机浮点数<br>
--- @param a number 最小值
--- @param b number 最大值
--- @return number 随机浮点数
lib.rnd.Float = function(a, b)
    if a > b then a, b = b, a end
    local c = (a + b) / 2
    return c + (math.random() - 0.5) * (b - c) * 2
end

--- 返回一个a~b之间的随机整数<br>
--- @param a number 最小值
--- @param b number 最大值
--- @return number 随机整数
lib.rnd.Int = function(a, b)
    if a > b then a, b = b, a end
    return math.random(a, b)
end

--- 返回一个-1或1的随机符号<br>
--- @return number -1或1
lib.rnd.Sign = function()
    return ({-1, 1})[math.random(2)]
end


return lib