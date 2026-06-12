LoadImageFromFile('void_charge_item', 'void_resource/void_charge_item.png')
LoadPS('void_charge_in', 'void_resource/void_charge_in_psi.psi', 'void_charge_item')

void_charge = Class(object)

function void_charge:init(master, x, y, range, dur)
    if IsValid(master) then
        self.x, self.y = master.x, master.y
    else
        self.x, self.y = x, y
    end
    range = range or 270
    dur = dur or 45
    self.master = master
    self.bound = false
    self.range = range
    self.dur = int(dur)
    self.ang = ran:Float(0, 360)
end

function void_charge:frame()
    local dur = self.dur
    local range = self.range
    if IsValid(self.master) then
        self.x, self.y = self.master.x, self.master.y
    end
    if self.timer == 0 then
        local a = self.ang
        for i = 1, 3 do
            New(void_charge_in, self, a + 120 * i, a + 120 * i + 240,range, 0, int(dur / 2))
        end
    elseif self.timer == int(dur / 4) then
        local a = self.ang + 180
        for i = 1, 3 do
            New(void_charge_in, self, a + 120 * i, a + 120 * i - 360,range, 0, int(dur / 2) - int(dur / 4))
        end
    elseif self.timer == dur then
        local a = ran:Float(0, 360)
    elseif self.timer >= 180 then
        Del(self)
    end
end

void_charge_in = Class(object)

function void_charge_in:init(master, st_a, ed_a, st_d, ed_d, lt)
    if IsValid(master) then
        self.x, self.y = master.x + cos(st_a) * st_d, master.y + sin(st_a) * st_d
    else
        Del(self)
    end
    self.layer = LAYER_ENEMY_BULLET_EF + 5
    self.master = master
    self.st_a = st_a
    self.ed_a = ed_a
    self.st_d = st_d
    self.ed_d = ed_d
    self.lt = lt
    self.img = 'void_charge_in'
    self.rot = st_a + 90
    self.bound = false
end

function void_charge_in:frame()
    local a = self.st_a + (self.ed_a - self.st_a) * min(self.timer / self.lt, 1)
    local d = self.st_d + (self.ed_d - self.st_d) * min(self.timer / self.lt, 1)
    if IsValid(self.master) then
        self.x, self.y = self.master.x + cos(a) * d, self.master.y + sin(a) * d
        self.rot = a + 90
    else
        Del(self)
    end
    if self.timer > self.lt then
        ParticleStop(self)
    end
    if self.timer > 120 then
        Del(self)
    end
end