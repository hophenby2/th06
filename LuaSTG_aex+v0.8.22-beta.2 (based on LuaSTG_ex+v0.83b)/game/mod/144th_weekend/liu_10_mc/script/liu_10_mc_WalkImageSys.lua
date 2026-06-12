local lib = {}
-------------------------------------
local calc = require("liu_10_mc.script.liu_10_mc_math")
local draw = require("liu_10_mc.script.liu_10_mc_draw")
local func = calc.lerp
-------------------------------------
local wisys = plus.Class()
function wisys:init(obj, func_list, state, dmgmaxt)
    self.tex = ""
    self.sprite = {x = 0, y = 0, w = 0, h = 0}
    self.anchor = {0, 0}
    self.obj = obj
    self.hs, self.vs = 1, 1
    self.rot, self.omiga = 0, 0
    self.tmp_rot = self.rot
    self.func_list = func_list
    self.state_list = state
    self.act_state = state[1] or "normal"
    self.tmp_state = self.act_state
    self.count = -1
    self.img_dx, self.img_dy = 0, 0
    self.tmp_dx, self.tmp_dy = self.img_dx, self.img_dy
    self.cenX, self.cenY = 0, 0
    self.obj.dmgmaxt = dmgmaxt or 0
    self.loop_script = false
    self.no_change = false
    self.obj.A, self.obj.B = 16, 16
end
function wisys:frame()
    local obj = self.obj
    if not IsValid(obj) then
        return
    end
    local state = self.state_list
    if #state >= 5 then
        if sign(obj.dx) == -1 and self.no_change == false then
            self.act_state = state[2]
        end
        if sign(obj.dx) == 1 and self.no_change == false then
            self.act_state = state[3]
        end
        if sign(obj.dx) == 0 and self.act_state == state[2] and self.no_change == false then
            self.act_state = state[4]
        end
        if sign(obj.dx) == 0 and self.act_state == state[3] and self.no_change == false then
            self.act_state = state[5]
        end
    end
    if self.tmp_state ~= self.act_state then
        self.anchor = {0, 0}
        self.img_dx, self.img_dy = 0, 0
        self.tmp_dx, self.tmp_dy = self.img_dx, self.img_dy
        self.cenX, self.cenY = 0, 0
        self.hs, self.vs = 1, 1
        self.rot, self.omiga = 0, 0
        self.loop_script = false
        self.count = -1
    end
    for i = 1, #state do
        if self.act_state == state[i] then
            self.func_list[i](self, obj)
            break
        end
    end
    self.rot = self.rot + self.omiga
    if self.tmp_rot ~= self.rot then
        self.tmp_rot = self.rot
    end
    self.count = self.count + 1
    self.tmp_state = self.act_state
    if type(obj.A) == "number" and type(obj.B) == "number" and obj.colli then
        obj.a, obj.b = obj.A, obj.B
        if obj.a == 0 and obj.b == 0 then
            obj.colli = false
        else
            obj.colli = true
        end
        if IsValid(obj.Hitbox) or obj.Hitbox then
            obj.group = GROUP_NONTJT
        else
            obj.group = GROUP_ENEMY
        end
    end
end
function wisys:render(dmgt, dmgmaxt)
    local obj = self.obj
    if not IsValid(obj) then
        return
    end
    local co = Color(0xFFFFFFFF)
    local c = 0
    if dmgt and dmgmaxt then
        c = dmgt / dmgmaxt
    end
    local dmgt_condition = obj._blend and obj._a and obj._r and obj._g and obj._b
    if dmgt_condition then
        co = Color(obj._a, obj._r - obj._r * 0.75 * c, obj._g - obj._g * 0.75 * c, obj._b)
    else
        co = Color(255, 255 - 255 * 0.75 * c, 255 - 255 * 0.75 * c, 255)
    end
    local tex = self.tex
    if tex == "" or not tex then
        return
    end
    local sprite = self.sprite
    local anchor = self.anchor
    local dx, dy = (sprite.dx or 0), (sprite.dy or 0)
    local x, y = obj.x + self.img_dx + dx , obj.y + self.img_dy - dy
    local hs, vs = obj.hscale * self.hs, obj.vscale * self.vs
    local rot = self.rot
    local tx, ty, tw, th = sprite.x, sprite.y, sprite.w, sprite.h
    local w, h = {tw / 2 + self.cenX * 1, tw / 2 + self.cenX * -1}, {th / 2 + self.cenY * 1, th / 2 + self.cenY * -1}
    if anchor[1] == 1 then
        w = {0 + self.cenX * 1, tw + self.cenX * -1}
    elseif anchor[1] == 2 then
        w = {tw + self.cenX * 1, 0 + self.cenX * -1}
    end
    if anchor[2] == 1 then
        h = {0 + self.cenY * 1,th + self.cenY * -1}
    elseif anchor[2] == 2 then
        h = {th + self.cenY * 1, 0 + self.cenY * -1}
    end
    w[1], w[2], h[1], h[2] = w[1] * hs * -1,w[2] * hs * 1, h[1] * vs * 1, h[2] * vs * -1
    local rect = {
        {w[1] * cos(rot) - h[1] * sin(rot), w[1] * sin(rot) + h[1] * cos(rot)},
        {w[2] * cos(rot) - h[1] * sin(rot), w[2] * sin(rot) + h[1] * cos(rot)},
        {w[2] * cos(rot) - h[2] * sin(rot), w[2] * sin(rot) + h[2] * cos(rot)},
        {w[1] * cos(rot) - h[2] * sin(rot), w[1] * sin(rot) + h[2] * cos(rot)},
    }
    RenderTexture(tex, obj._blend or "",
        {x + rect[1][1], y + rect[1][2], 0.5, tx + 0, ty + 0, co},
        {x + rect[2][1], y + rect[2][2], 0.5, tx + tw, ty + 0, co},
        {x + rect[3][1], y + rect[3][2], 0.5, tx + tw, ty + th, co},
        {x + rect[4][1], y + rect[4][2], 0.5, tx + 0, ty + th, co})
end
-------------------------------------
lib.wisys = wisys

function lib:FilpX()
    self.hs = self.hs * -1
end

function lib:FilpY()
    self.vs = self.vs * -1
end

function lib:Pos(x, y)
    self.img_dx, self.img_dy = x, y
    self.tmp_dx, self.tmp_dy = self.img_dx, self.img_dy
end
function lib:Rotate(rot)
    self.rot = rot
    self.tmp_rot = self.rot
end
function lib:PosTime(t, maxt, mode, x, y)
    self.img_dx = func(self.tmp_dx, x, min(t / maxt, 1), mode)
    self.img_dy = func(self.tmp_dy, y, min(t / maxt, 1), mode)
    if t >= (maxt - 1) then
        self.tmp_dx, self.tmp_dy = self.img_dx, self.img_dy
    end
end
function lib:RotateTime(t, maxt, mode, rot)
    self.tmp_rot = (self.tmp_rot + 180) % 360 - 180
    self.rot = func(self.tmp_rot, rot, min(t / maxt, 1), mode)
    if t >= (maxt - 1) then
        self.tmp_rot = self.rot
    end
end
function lib:AngleVel(vel)
    self.omiga = vel
end
function lib:Anchor(h, v)
    self.anchor = {h, v}
end
function lib:AnchorOffset(dx, dy)
    self.cenX, self.cenY = dx, dy
end
function lib:SetHitBox(w, h)
	if IsValid(self.obj) then
		local obj = self.obj
		obj.A = w / 2
		obj.B = h / 2
	end
end

function lib:SetWalkImage(list, id, t, hs, vs, rot, omiga)
    local p = list[id]
    self.tex = p.sprite.tex
    for _, v in ipairs(p) do
        if t == v[1] then
            local walk = self.sprite
            walk.x, walk.y, walk.w, walk.h = unpack(v[2])
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
-------------------------------------
return lib