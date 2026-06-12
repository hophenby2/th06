-- Auto-generated LuaSTG approximation from ECL IR
-- source: th062/th12/stage06.decl
-- This is a semantic draft: timings/bullets are approximate and intended for manual refinement.
local M = {}
local ecl_var = setmetatable({}, { __index = function() return 0 end })
local function ecl_rad(value) return (value or 0) * 180 / math.pi end
local function ecl_sync_self(self)
    if self then ecl_var[-9997], ecl_var[-9996] = self.x or 0, self.y or 0 end
end
local function ecl_pick_rank(easy, normal, hard, lunatic)
    local rank = _G.difficulty or (lstg and lstg.var and (lstg.var.difficulty or lstg.var.rank)) or 2
    if type(rank) == 'string' then
        local key = string.lower(rank)
        rank = ({easy = 1, e = 1, normal = 2, n = 2, hard = 3, h = 3, lunatic = 4, l = 4})[key] or 2
    end
    local values = {easy, normal, hard, lunatic}
    return values[math.max(1, math.min(4, math.floor(rank or 2)))] or normal or easy or 0
end
local ecl_Boss, ecl_Boss1, ecl_Boss1_at1, ecl_Boss1_at1b, ecl_Boss2, ecl_Boss2_at1, ecl_Boss2_at1h, ecl_Boss2_at2, ecl_Boss3, ecl_Boss3_at1, ecl_Boss3_at1e1, ecl_Boss3_at1e2, ecl_Boss3_at1e3, ecl_Boss3_at1e4, ecl_Boss4, ecl_Boss4_at1, ecl_Boss4_at1e1, ecl_Boss4_at1e2, ecl_Boss4_at1e3, ecl_Boss4_at1e4, ecl_Boss5, ecl_Boss6, ecl_BossCard1, ecl_BossCard1_at1, ecl_BossCard1_at1h, ecl_BossCard1_at2, ecl_BossCard1_at2h, ecl_BossCard2, ecl_BossCard2_at1, ecl_BossCard2_at2, ecl_BossCard3, ecl_BossCard3_at, ecl_BossCard3_at2, ecl_BossCard3_at2b, ecl_BossCard4, ecl_BossCard4_at, ecl_BossCard4_at2, ecl_BossCard4_at3, ecl_BossCard4_at4, ecl_BossCard4_at5, ecl_BossCard4_at6, ecl_BossCard4_at7, ecl_BossCard5, ecl_BossCard5_at, ecl_BossCard6, ecl_BossCard6_at, ecl_BossCard6_atLine, ecl_BossCard6_atLineDead, ecl_BossEyes, ecl_BossEyes2, ecl_HPWait

function ecl_Boss(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    -- boss/meta ins_424(24)
    -- unsupported ins_412(0)
    -- visual/helper ins_258(2)
    -- visual/helper ins_262(0, 0)
    -- unsupported ins_402(76)
    self.x, self.y = 64.0, 64.0
    ecl_sync_self(self)
    -- unsupported ins_401(64.0f, 64.0f)
    -- unsupported ins_415(60)
    self.hp, self.maxhp = 13200, 13200
    task.MoveTo(0.0, 112.0, 60, 4)
    ecl_sync_self(self)
    -- +60:
    -- unsupported ins_419()
    SetV2(self, 112.0, 0.0, true, false)
    -- visual/helper ins_258(0)
    -- visual/helper ins_259(1, 95)
    -- visual/helper ins_259(2, 158)
    -- visual/helper ins_258(2)
    -- unsupported ins_526(160.0f, 16748543)
    ecl_Boss1(self)
    do return end
end
M.Boss = ecl_Boss

function ecl_Boss1(self)
    ecl_sync_self(self)
    -- timerReset
    -- setInterrupt phase=0 life=2200 time=2640 sub="BossCard1"
    -- boss/meta ins_427(0, 2200.0f, -24448)
    -- boss/meta ins_424(24)
    -- visual/helper ins_440(5)
    -- visual/helper ins_258(2)
    -- visual/helper ins_263(0, 119)
    task._Wait(10)
    ecl_var[-9978] = 0.098175
    while true do
        -- visual/helper ins_269(0)
        -- visual/helper ins_416(31)
        task._Wait(60)
        task.New(self, function() ecl_Boss1_at1(self) end)
        -- unsupported ins_448(100, 100, 80, 60)
        task.New(self, _editor_tasks["liu_10_mc_moveRand"](60, 4, 3.0))
        task._Wait(70)
        -- visual/helper ins_269(0)
        -- visual/helper ins_416(31)
        task._Wait(60)
        task.New(self, function() ecl_Boss1_at1b(self) end)
        -- unsupported ins_448(100, 100, 80, 60)
        task.New(self, _editor_tasks["liu_10_mc_moveRand"](60, 4, 3.0))
        task._Wait(70)
    end
    do return end
end
M.Boss1 = ecl_Boss1

function ecl_Boss1_at1(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etAim et=0 mode=3
    -- etSprite et=0 style=0 color=6
    -- etCountD et=0 ways=ecl_pick_rank(6, 12, 14, 14) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=0 speed=ecl_pick_rank(3.0, 3.0, 4.0, 4.4) step=ecl_pick_rank(3.5, 1.5, 1.5, 1.5)
    -- etNew(1)
    -- etAim et=1 mode=3
    -- etSprite et=1 style=3 color=6
    -- etCountD et=1 ways=ecl_pick_rank(6, 12, 14, 14) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=1 speed=ecl_pick_rank(3.0, 3.0, 4.0, 4.4) step=ecl_pick_rank(3.5, 1.5, 1.5, 1.5)
    -- etNew(2)
    -- etAim et=2 mode=3
    -- etSprite et=2 style=17 color=3
    -- etCountD et=2 ways=ecl_pick_rank(6, 12, 14, 14) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=2 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=2 speed=ecl_pick_rank(3.0, 3.0, 4.0, 4.4) step=ecl_pick_rank(3.5, 1.5, 1.5, 1.5)
    -- etNew(3)
    -- etAim et=3 mode=3
    -- etSprite et=3 style=26 color=1
    -- etCountD et=3 ways=ecl_pick_rank(6, 12, 14, 14) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=3 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=3 speed=ecl_pick_rank(3.0, 3.0, 4.0, 4.4) step=ecl_pick_rank(1.5, 1.5, 1.5, 1.5)
    -- etOffsetAbs et=0 x=ecl_var[-9997] y=ecl_var[-9996] - (32)
    -- etOffsetAbs et=1 x=ecl_var[-9997] y=ecl_var[-9996] - (32)
    -- etOffsetAbs et=2 x=ecl_var[-9997] y=ecl_var[-9996] - (32)
    -- etOffsetAbs et=3 x=ecl_var[-9997] y=ecl_var[-9996] - (32)
    v_C = 0
    i_D = 3
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        v_A = v_C
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.060415
        v_B = v_A
        -- etAngle et=2 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.060415
        -- etAngle et=3 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.060415
        liu_10_mc.bullet.ShotBulletMode(3, 1, _editor_class["ecl_stage06_boss_Bullet_3_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 2, _editor_class["ecl_stage06_boss_Bullet_17_3"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 3, _editor_class["ecl_stage06_boss_Bullet_26_1"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(1.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- unsupported ins_448(20, 20, 15, 11)
        v_A = v_B
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.060415
        -- etAngle et=2 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.060415
        -- etAngle et=3 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.060415
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 1, _editor_class["ecl_stage06_boss_Bullet_3_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 2, _editor_class["ecl_stage06_boss_Bullet_17_3"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 3, _editor_class["ecl_stage06_boss_Bullet_26_1"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(1.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- unsupported ins_448(20, 20, 15, 11)
        v_C = v_C - 0.15708
        v_C = v_C - 0.392699
        v_B = v_B + 0.15708
        v_B = v_B + 0.392699
    end
    do return end
end
M.Boss1_at1 = ecl_Boss1_at1

function ecl_Boss1_at1b(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etAim et=0 mode=3
    -- etSprite et=0 style=0 color=6
    -- etCountD et=0 ways=ecl_pick_rank(6, 12, 14, 14) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=0 speed=ecl_pick_rank(3.0, 3.0, 4.0, 4.4) step=ecl_pick_rank(3.5, 1.5, 1.5, 1.5)
    -- etNew(1)
    -- etAim et=1 mode=3
    -- etSprite et=1 style=3 color=6
    -- etCountD et=1 ways=ecl_pick_rank(6, 12, 14, 14) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=1 speed=ecl_pick_rank(3.0, 3.0, 4.0, 4.4) step=ecl_pick_rank(3.5, 1.5, 1.5, 1.5)
    -- etNew(2)
    -- etAim et=2 mode=3
    -- etSprite et=2 style=17 color=3
    -- etCountD et=2 ways=ecl_pick_rank(6, 12, 14, 14) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=2 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=2 speed=ecl_pick_rank(3.0, 3.0, 4.0, 4.4) step=ecl_pick_rank(3.5, 1.5, 1.5, 1.5)
    -- etNew(3)
    -- etAim et=3 mode=3
    -- etSprite et=3 style=26 color=1
    -- etCountD et=3 ways=ecl_pick_rank(6, 12, 14, 14) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=3 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=3 speed=ecl_pick_rank(3.0, 3.0, 4.0, 4.4) step=ecl_pick_rank(1.5, 1.5, 1.5, 1.5)
    -- etOffsetAbs et=0 x=ecl_var[-9997] y=ecl_var[-9996] - (32)
    -- etOffsetAbs et=1 x=ecl_var[-9997] y=ecl_var[-9996] - (32)
    -- etOffsetAbs et=2 x=ecl_var[-9997] y=ecl_var[-9996] - (32)
    -- etOffsetAbs et=3 x=ecl_var[-9997] y=ecl_var[-9996] - (32)
    v_C = 0
    i_D = 3
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        v_A = v_C
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.060415
        v_B = v_A
        -- etAngle et=2 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.060415
        -- etAngle et=3 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A - 0.060415
        liu_10_mc.bullet.ShotBulletMode(3, 1, _editor_class["ecl_stage06_boss_Bullet_3_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 2, _editor_class["ecl_stage06_boss_Bullet_17_3"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 3, _editor_class["ecl_stage06_boss_Bullet_26_1"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(1.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- unsupported ins_448(20, 20, 15, 11)
        v_A = v_B
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.03927
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.060415
        -- etAngle et=2 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.060415
        -- etAngle et=3 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        v_A = v_A + 0.060415
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_0_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 1, _editor_class["ecl_stage06_boss_Bullet_3_6"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 2, _editor_class["ecl_stage06_boss_Bullet_17_3"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(3.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        liu_10_mc.bullet.ShotBulletMode(3, 3, _editor_class["ecl_stage06_boss_Bullet_26_1"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(6, 12, 14, 14))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(3.0, 3.0, 4.0, 4.4), ecl_pick_rank(1.5, 1.5, 1.5, 1.5), ecl_rad(v_A), ecl_rad(0.0), nil)
        -- unsupported ins_448(20, 20, 15, 11)
        v_C = v_C + 0.15708
        v_C = v_C + 0.392699
        v_B = v_B - 0.15708
        v_B = v_B - 0.392699
    end
    do return end
end
M.Boss1_at1b = ecl_Boss1_at1b

function ecl_Boss2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B = 0, 0, 0, 0
    self.hp, self.maxhp = 12400, 12400
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss2_228 @ 0;
    -- unsupported ins_512(640.0f)
    -- control-flow not structurally lowered: goto Boss2_248 @ 0;
    -- label Boss2_228
    -- unsupported ins_513(640.0f)
    -- label Boss2_248
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    -- setInterrupt phase=0 life=2400 time=2640 sub="BossCard2"
    -- boss/meta ins_427(0, 2400.0f, -24448)
    -- visual/helper ins_440(4)
    -- unsupported ins_415(240)
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss2_784 @ 0;
    -- unsupported ins_406()
    -- unsupported ins_407(1, 50)
    -- unsupported ins_407(2, 60)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    -- label Boss2_784
    -- visual/helper ins_416(28)
    SetV2(self, 112.0, 0.0, true, false)
    task.MoveTo(0.0, 128.0, 60, 0)
    ecl_sync_self(self)
    task._Wait(90)
    -- visual/helper ins_263(0, 119)
    -- visual/helper ins_416(31)
    task._Wait(90)
    -- visual/helper ins_416(58)
    -- visual/helper ins_259(3, 48)
    -- visual/helper ins_259(4, 57)
    -- visual/helper ins_259(5, 49)
    -- visual/helper ins_259(6, 50)
    -- visual/helper ins_259(7, 51)
    -- visual/helper ins_259(8, 52)
    -- visual/helper ins_259(9, 53)
    -- visual/helper ins_259(10, 54)
    -- visual/helper ins_259(11, 55)
    -- visual/helper ins_259(12, 56)
    -- unsupported ins_281(3, 0)
    -- unsupported ins_281(4, 0)
    -- unsupported ins_281(5, 0)
    -- unsupported ins_281(6, 0)
    -- unsupported ins_281(7, 0)
    -- unsupported ins_281(8, 0)
    -- unsupported ins_281(9, 0)
    -- unsupported ins_281(10, 0)
    -- unsupported ins_281(11, 0)
    -- unsupported ins_281(12, 0)
    task.New(self, function() ecl_BossEyes(self) end)
    task._Wait(60)
    -- visual/helper ins_416(28)
    task._Wait(20)
    ecl_var[-9978] = 0.098175
    task.New(self, function() ecl_Boss2_at2(self) end)
    while true do
        -- visual/helper ins_416(31)
        task._Wait(60)
        task.New(self, function() ecl_Boss2_at1(self) end)
        -- control-flow not structurally lowered: unless ([-9959] >= 2) goto Boss2_2076 @ 0;
        task._Wait(20)
        task.New(self, function() ecl_Boss2_at1h(self, 0.09817477) end)
        task._Wait(20)
        task.New(self, function() ecl_Boss2_at1h(self, 0.09817477) end)
        task._Wait(20)
        task.New(self, function() ecl_Boss2_at1h(self, 0.1308997) end)
        task._Wait(20)
        task.New(self, function() ecl_Boss2_at1h(self, 0.1308997) end)
        task._Wait(60)
        -- control-flow not structurally lowered: goto Boss2_2116 @ 0;
        -- label Boss2_2076
        task._Wait(100)
        task._Wait(70)
    end
    do return end
end
M.Boss2 = ecl_Boss2

function ecl_Boss2_at1(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C = 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etSprite et=0 style=7 color=2
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=0 speed=8.0 step=8.0
    -- laser ins_600(0, 0.0f, 512.0f, 16.0f, 16.0f) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- laser ins_601(0, 60, 16, 60, 15, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- unsupported ins_508(0, 19, -1)
    -- etOffset et=0 x=-114.0 y=54.0
    v_B = ecl_var[-9997] + (-114)
    v_C = ecl_var[-9996] + (54)
    -- unsupported ins_520(%A, %B, %C)
    -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
    -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- etOffset et=0 x=114.0 y=54.0
    v_B = ecl_var[-9997] + (114)
    v_C = ecl_var[-9996] + (54)
    -- unsupported ins_520(%A, %B, %C)
    -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
    -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- etOffset et=0 x=-64.0 y=-80.0
    v_B = ecl_var[-9997] + (-64)
    v_C = ecl_var[-9996] + (-80)
    -- unsupported ins_520(%A, %B, %C)
    -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
    -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- etOffset et=0 x=64.0 y=-80.0
    v_B = ecl_var[-9997] + (64)
    v_C = ecl_var[-9996] + (-80)
    -- unsupported ins_520(%A, %B, %C)
    -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
    -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    do return end
end
M.Boss2_at1 = ecl_Boss2_at1

function ecl_Boss2_at1h(self, v_A)
    ecl_sync_self(self)
    local i_A = v_A or 0
    local v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etSprite et=0 style=7 color=2
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=0 speed=8.0 step=8.0
    -- laser ins_600(0, 0.0f, 512.0f, 16.0f, 16.0f) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- laser ins_601(0, 60, 16, 60, 15, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- unsupported ins_508(0, 19, -1)
    -- etOffset et=0 x=-114.0 y=54.0
    v_C = ecl_var[-9997] + (-114)
    v_D = ecl_var[-9996] + (54)
    -- unsupported ins_520(%B, %C, %D)
    v_B = v_B + (v_A * ecl_var[-9987])
    -- etAngle et=0 angle=ecl_rad(v_B) step=ecl_rad(0.0)
    -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- etOffset et=0 x=114.0 y=54.0
    v_C = ecl_var[-9997] + (114)
    v_D = ecl_var[-9996] + (54)
    -- unsupported ins_520(%B, %C, %D)
    v_B = v_B + (v_A * ecl_var[-9987])
    -- etAngle et=0 angle=ecl_rad(v_B) step=ecl_rad(0.0)
    -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- etOffset et=0 x=-64.0 y=-80.0
    v_C = ecl_var[-9997] + (-64)
    v_D = ecl_var[-9996] + (-80)
    -- unsupported ins_520(%B, %C, %D)
    v_B = v_B + (v_A * ecl_var[-9987])
    -- etAngle et=0 angle=ecl_rad(v_B) step=ecl_rad(0.0)
    -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- etOffset et=0 x=64.0 y=-80.0
    v_C = ecl_var[-9997] + (64)
    v_D = ecl_var[-9996] + (-80)
    -- unsupported ins_520(%B, %C, %D)
    v_B = v_B + (v_A * ecl_var[-9987])
    -- etAngle et=0 angle=ecl_rad(v_B) step=ecl_rad(0.0)
    -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    do return end
end
M.Boss2_at1h = ecl_Boss2_at1h

function ecl_Boss2_at2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E, v_F, i_F = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    task._Wait(60)
    -- unsupported ins_435($D, 6, 12, 12, 12)
    -- etNew(1)
    -- etAim et=1 mode=0
    -- etSprite et=1 style=29 color=0
    -- etCount et=1 ways=i_D layers=1
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.28559932)
    -- etSpeed et=1 speed=5.0 step=3.5
    -- etEx et=1 params preserved
    -- etEx et=1 params preserved
    -- unsupported ins_436(%E, 2.0f, 2.0f, 2.0f, 3.0f)
    i_D = i_D - 1
    i_F = 6000
    for _ecl_loop = 1, math.max(0, math.floor(i_F)) do
        -- etEx et=1 params preserved
        -- etAngle et=1 angle=ecl_rad(0 / (5)) step=ecl_rad(3.1415927 / (i_D))
        liu_10_mc.bullet.ShotBulletMode(0, 1, _editor_class["ecl_stage06_boss_Bullet_29_0"], self.x, self.y, (ecl_var[-9997]) - self.x, (ecl_var[-9996] - (32)) - self.y, 0, 0, 0, math.max(1, math.floor(i_D)), math.max(1, math.floor(1)), 5.0, 3.5, ecl_rad(0 / (5)), ecl_rad(3.1415927 / (i_D)), {{2, 0, 64, 60, 1, ecl_var[-9989], v_E}})
        -- unsupported ins_448(20, 20, 20, 17)
        v_C = v_C - 0.15708
    end
    do return end
end
M.Boss2_at2 = ecl_Boss2_at2

function ecl_Boss3(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    self.hp, self.maxhp = 12500, 12500
    -- visual/helper ins_259(3, -1)
    -- visual/helper ins_259(4, -1)
    -- visual/helper ins_259(5, -1)
    -- visual/helper ins_259(6, -1)
    -- visual/helper ins_259(7, -1)
    -- visual/helper ins_259(8, -1)
    -- visual/helper ins_259(9, -1)
    -- visual/helper ins_259(10, -1)
    -- visual/helper ins_259(11, -1)
    -- visual/helper ins_259(12, -1)
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss3_468 @ 0;
    -- unsupported ins_512(640.0f)
    -- control-flow not structurally lowered: goto Boss3_488 @ 0;
    -- label Boss3_468
    -- unsupported ins_513(640.0f)
    -- label Boss3_488
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    -- unsupported ins_405()
    self.x, self.y = 0.0, 192.0
    ecl_sync_self(self)
    -- setInterrupt phase=0 life=2500 time=2700 sub="BossCard3"
    -- boss/meta ins_427(0, 2500.0f, -24448)
    -- visual/helper ins_440(3)
    -- unsupported ins_415(120)
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss3_2128 @ 0;
    v_C = ecl_var[-9997]
    v_D = ecl_var[-9996]
    self.x, self.y = v_C + (-114), v_D + (54)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 20)
    -- unsupported ins_407(2, 10)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (114), v_D + (54)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 20)
    -- unsupported ins_407(2, 10)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (-64), v_D + (-80)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 20)
    -- unsupported ins_407(2, 10)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (64), v_D + (-80)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 20)
    -- unsupported ins_407(2, 10)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C, v_D
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 20)
    -- unsupported ins_407(2, 20)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    -- label Boss3_2128
    -- visual/helper ins_416(28)
    task._Wait(120)
    -- visual/helper ins_416(58)
    -- visual/helper ins_259(3, 48)
    -- visual/helper ins_259(4, 57)
    -- visual/helper ins_259(5, 49)
    -- visual/helper ins_259(6, 50)
    -- visual/helper ins_259(7, 51)
    -- visual/helper ins_259(8, 52)
    -- visual/helper ins_259(9, 53)
    -- visual/helper ins_259(10, 54)
    -- visual/helper ins_259(11, 55)
    -- visual/helper ins_259(12, 56)
    -- unsupported ins_281(3, 0)
    -- unsupported ins_281(4, 0)
    -- unsupported ins_281(5, 0)
    -- unsupported ins_281(6, 0)
    -- unsupported ins_281(7, 0)
    -- unsupported ins_281(8, 0)
    -- unsupported ins_281(9, 0)
    -- unsupported ins_281(10, 0)
    -- unsupported ins_281(11, 0)
    -- unsupported ins_281(12, 0)
    task.New(self, function() ecl_BossEyes(self) end)
    task.MoveTo(0.0, 128.0, 60, 0)
    ecl_sync_self(self)
    task._Wait(60)
    -- visual/helper ins_416(28)
    SetV2(self, 96.0, 0.0, true, false)
    -- visual/helper ins_258(2)
    -- visual/helper ins_262(0, 0)
    -- visual/helper ins_263(0, 119)
    -- visual/helper ins_416(31)
    task._Wait(60)
    while true do
        task.New(self, function() ecl_Boss3_at1(self) end)
        task.New(self, function() ecl_Boss3_at1e1(self) end)
        task.New(self, function() ecl_Boss3_at1e2(self) end)
        task.New(self, function() ecl_Boss3_at1e3(self) end)
        task.New(self, function() ecl_Boss3_at1e4(self) end)
        task._Wait(20)
        task.New(self, _editor_tasks["liu_10_mc_moveRand"](60, 4, 0.5))
        -- unsupported ins_448(90, 90, 80, 80)
    end
    do return end
end
M.Boss3 = ecl_Boss3

function ecl_Boss3_at1(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etAim et=0 mode=1
    -- etSprite et=0 style=7 color=4
    -- etCount et=0 ways=1 layers=5
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=0 speed=3.0 step=2.7
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    v_A = -1.570796
    i_D = 60
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        v_B = math.cos(v_A + 1.5707964) * (32.0)
        v_C = math.sin(v_A + 1.5707964) * (32.0)
        -- etOffset et=0 x=v_B y=v_C
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        liu_10_mc.bullet.ShotBulletMode(1, 0, _editor_class["ecl_stage06_boss_Bullet_7_4"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(5)), 3.0, 2.7, ecl_rad(v_A), ecl_rad(v_A), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
        v_A = v_A + 0.19635
        task._Wait(1)
    end
    do return end
end
M.Boss3_at1 = ecl_Boss3_at1

function ecl_Boss3_at1e1(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(1)
    -- etAim et=1 mode=1
    -- etSprite et=1 style=7 color=13
    -- etCount et=1 ways=1 layers=5
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=1 speed=1.0 step=0.7
    -- etEx et=1 params preserved
    -- etEx et=1 params preserved
    -- etEx et=1 params preserved
    v_A = -1.5707964 + (0 / (16))
    -- unsupported ins_435($D, 30, 60, 60, 60)
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etOffsetAbs et=1 x=(-114) + ecl_var[-9997] y=(54) + ecl_var[-9996]
        v_B = math.cos(v_A + 1.5707964) * (16.0)
        v_C = math.sin(v_A + 1.5707964) * (16.0)
        -- etOffset et=1 x=v_B y=v_C
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        liu_10_mc.bullet.ShotBulletMode(1, 1, _editor_class["ecl_stage06_boss_Bullet_7_13"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(5)), 1.0, 0.7, ecl_rad(v_A), ecl_rad(v_A), {{2, 1, 4, 60, -999999, 0.033333335, -999.0}})
        v_A = v_A + 0.19635
        v_A = v_A + 0.19635
        -- unsupported ins_448(2, 1, 1, 1)
    end
    do return end
end
M.Boss3_at1e1 = ecl_Boss3_at1e1

function ecl_Boss3_at1e2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(2)
    -- etAim et=2 mode=1
    -- etSprite et=2 style=7 color=13
    -- etCount et=2 ways=1 layers=5
    -- etAngle et=2 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=2 speed=1.0 step=0.7
    -- etEx et=2 params preserved
    -- etEx et=2 params preserved
    -- etEx et=2 params preserved
    v_A = -1.5707964 + (0 / (16))
    -- unsupported ins_435($D, 30, 60, 60, 60)
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etOffsetAbs et=2 x=(114) + ecl_var[-9997] y=(54) + ecl_var[-9996]
        v_B = math.cos(v_A + 1.5707964) * (16.0)
        v_C = math.sin(v_A + 1.5707964) * (16.0)
        -- etOffset et=2 x=v_B y=v_C
        -- etAngle et=2 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        liu_10_mc.bullet.ShotBulletMode(1, 2, _editor_class["ecl_stage06_boss_Bullet_7_13"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(5)), 1.0, 0.7, ecl_rad(v_A), ecl_rad(v_A), {{2, 1, 4, 60, -999999, 0.033333335, -999.0}})
        v_A = v_A - 0.19635
        v_A = v_A - 0.19635
        -- unsupported ins_448(2, 1, 1, 1)
    end
    do return end
end
M.Boss3_at1e2 = ecl_Boss3_at1e2

function ecl_Boss3_at1e3(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(3)
    -- etAim et=3 mode=1
    -- etSprite et=3 style=7 color=2
    -- etCount et=3 ways=1 layers=5
    -- etAngle et=3 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=3 speed=1.0 step=0.7
    -- etEx et=3 params preserved
    -- etEx et=3 params preserved
    -- etEx et=3 params preserved
    v_A = 0.0 + (0 / (16))
    -- unsupported ins_435($D, 30, 60, 60, 60)
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etOffsetAbs et=3 x=(-64) + ecl_var[-9997] y=(-80) + ecl_var[-9996]
        v_B = math.cos(v_A + 1.5707964) * (16.0)
        v_C = math.sin(v_A + 1.5707964) * (16.0)
        -- etOffset et=3 x=v_B y=v_C
        -- etAngle et=3 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        liu_10_mc.bullet.ShotBulletMode(1, 3, _editor_class["ecl_stage06_boss_Bullet_7_2"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(5)), 1.0, 0.7, ecl_rad(v_A), ecl_rad(v_A), {{2, 1, 4, 60, -999999, 0.033333335, -999.0}})
        v_A = v_A - 0.19635
        v_A = v_A - 0.19635
        v_A = v_A - 0.098175
        -- unsupported ins_448(2, 1, 1, 1)
    end
    do return end
end
M.Boss3_at1e3 = ecl_Boss3_at1e3

function ecl_Boss3_at1e4(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(4)
    -- etAim et=4 mode=1
    -- etSprite et=4 style=7 color=2
    -- etCount et=4 ways=1 layers=5
    -- etAngle et=4 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=4 speed=1.0 step=0.7
    -- etEx et=4 params preserved
    -- etEx et=4 params preserved
    -- etEx et=4 params preserved
    v_A = 3.1415927 + (0 / (16))
    -- unsupported ins_435($D, 30, 60, 60, 60)
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etOffsetAbs et=4 x=(64) + ecl_var[-9997] y=(-80) + ecl_var[-9996]
        v_B = math.cos(v_A + 1.5707964) * (16.0)
        v_C = math.sin(v_A + 1.5707964) * (16.0)
        -- etOffset et=4 x=v_B y=v_C
        -- etAngle et=4 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        liu_10_mc.bullet.ShotBulletMode(1, 4, _editor_class["ecl_stage06_boss_Bullet_7_2"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(5)), 1.0, 0.7, ecl_rad(v_A), ecl_rad(v_A), {{2, 1, 4, 60, -999999, 0.033333335, -999.0}})
        v_A = v_A + 0.19635
        v_A = v_A + 0.19635
        v_A = v_A + 0.098175
        -- unsupported ins_448(2, 1, 1, 1)
    end
    do return end
end
M.Boss3_at1e4 = ecl_Boss3_at1e4

function ecl_Boss4(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    self.hp, self.maxhp = 22000, 22000
    -- visual/helper ins_259(3, -1)
    -- visual/helper ins_259(4, -1)
    -- visual/helper ins_259(5, -1)
    -- visual/helper ins_259(6, -1)
    -- visual/helper ins_259(7, -1)
    -- visual/helper ins_259(8, -1)
    -- visual/helper ins_259(9, -1)
    -- visual/helper ins_259(10, -1)
    -- visual/helper ins_259(11, -1)
    -- visual/helper ins_259(12, -1)
    -- unsupported ins_402(2)
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss4_488 @ 0;
    -- unsupported ins_512(640.0f)
    -- control-flow not structurally lowered: goto Boss4_508 @ 0;
    -- label Boss4_488
    -- unsupported ins_513(640.0f)
    -- label Boss4_508
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    -- unsupported ins_405()
    self.x, self.y = 0.0, 192.0
    ecl_sync_self(self)
    -- setInterrupt phase=0 life=5000 time=4200 sub="BossCard4"
    -- boss/meta ins_427(0, 5000.0f, -24448)
    -- visual/helper ins_440(2)
    -- unsupported ins_415(120)
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss4_2148 @ 0;
    v_C = ecl_var[-9997]
    v_D = ecl_var[-9996]
    self.x, self.y = v_C + (-114), v_D + (54)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 10)
    -- unsupported ins_407(2, 13)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (114), v_D + (54)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 10)
    -- unsupported ins_407(2, 13)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (-64), v_D + (-80)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 10)
    -- unsupported ins_407(2, 13)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (64), v_D + (-80)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 10)
    -- unsupported ins_407(2, 13)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C, v_D
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 20)
    -- unsupported ins_407(2, 25)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    -- label Boss4_2148
    -- visual/helper ins_416(28)
    task._Wait(120)
    -- visual/helper ins_416(58)
    -- visual/helper ins_259(3, 48)
    -- visual/helper ins_259(4, 57)
    -- visual/helper ins_259(5, 49)
    -- visual/helper ins_259(6, 50)
    -- visual/helper ins_259(7, 51)
    -- visual/helper ins_259(8, 52)
    -- visual/helper ins_259(9, 53)
    -- visual/helper ins_259(10, 54)
    -- visual/helper ins_259(11, 55)
    -- visual/helper ins_259(12, 56)
    -- unsupported ins_281(3, 0)
    -- unsupported ins_281(4, 0)
    -- unsupported ins_281(5, 0)
    -- unsupported ins_281(6, 0)
    -- unsupported ins_281(7, 0)
    -- unsupported ins_281(8, 0)
    -- unsupported ins_281(9, 0)
    -- unsupported ins_281(10, 0)
    -- unsupported ins_281(11, 0)
    -- unsupported ins_281(12, 0)
    task.New(self, function() ecl_BossEyes(self) end)
    task.MoveTo(0.0, 96.0, 120, 0)
    ecl_sync_self(self)
    task._Wait(60)
    -- visual/helper ins_416(28)
    -- visual/helper ins_258(2)
    -- visual/helper ins_262(0, 0)
    -- visual/helper ins_263(0, 119)
    -- visual/helper ins_416(31)
    task._Wait(60)
    task._Wait(60)
    self.x, self.y = 0.0, 224.0
    ecl_sync_self(self)
    -- unsupported ins_308(-1.5707964f, 0.0f, 128.0f, 0.0f)
    i_E = 2
    for _ecl_loop = 1, math.max(0, math.floor(i_E)) do
        task.New(self, function() ecl_Boss4_at1e3(self) end)
        task._Wait(40)
        task.New(self, function() ecl_Boss4_at1e2(self) end)
        task._Wait(40)
        task.New(self, function() ecl_Boss4_at1e1(self) end)
        task._Wait(40)
        task.New(self, function() ecl_Boss4_at1e4(self) end)
        task._Wait(40)
    end
    -- unsupported ins_309(60, 0, 0.007853982f, -999999.0f, -999999.0f)
    while true do
        task.New(self, function() ecl_Boss4_at1e3(self) end)
        task._Wait(40)
        task.New(self, function() ecl_Boss4_at1e2(self) end)
        task._Wait(40)
        task.New(self, function() ecl_Boss4_at1e1(self) end)
        task._Wait(40)
        task.New(self, function() ecl_Boss4_at1e4(self) end)
        task._Wait(40)
    end
    do return end
end
M.Boss4 = ecl_Boss4

function ecl_Boss4_at1(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etAim et=0 mode=1
    -- etSprite et=0 style=7 color=4
    -- etCount et=0 ways=1 layers=1
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=0 speed=3.0 step=2.7
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    v_A = -1.570796
    i_D = 60
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        v_B = math.cos(v_A + 1.5707964) * (32.0)
        v_C = math.sin(v_A + 1.5707964) * (32.0)
        -- etOffset et=0 x=v_B y=v_C
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        liu_10_mc.bullet.ShotBulletMode(1, 0, _editor_class["ecl_stage06_boss_Bullet_7_4"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), 3.0, 2.7, ecl_rad(v_A), ecl_rad(v_A), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
        v_A = v_A + 0.19635
        task._Wait(1)
    end
    do return end
end
M.Boss4_at1 = ecl_Boss4_at1

function ecl_Boss4_at1e1(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(1)
    -- etAim et=1 mode=1
    -- etSprite et=1 style=7 color=13
    -- etCount et=1 ways=1 layers=3
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=1 speed=1.2 step=1.0
    -- etEx et=1 params preserved
    -- etEx et=1 params preserved
    -- etEx et=1 params preserved
    v_A = (ecl_var[-9989] + 3.1415927) + (0 / (16))
    i_D = 0
    i_E = 32
    for _ecl_loop = 1, math.max(0, math.floor(i_E)) do
        -- etOffsetAbs et=1 x=(-114) + ecl_var[-9997] y=(54) + ecl_var[-9996]
        v_B = math.cos(v_A + 1.5707964) * (16.0)
        v_C = math.sin(v_A + 1.5707964) * (16.0)
        -- etOffset et=1 x=v_B y=v_C
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        -- control-flow not structurally lowered: unless ((($D % 2) == 0) || ([-9959] >= 1)) goto Boss4_at1e1_1080 @ 0;
        liu_10_mc.bullet.ShotBulletMode(1, 1, _editor_class["ecl_stage06_boss_Bullet_7_13"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(3)), 1.2, 1.0, ecl_rad(v_A), ecl_rad(v_A), {{2, 1, 4, 60, -999999, 0.033333335, -999.0}})
        -- label Boss4_at1e1_1080
        v_A = v_A + 0.19635
        task._Wait(1)
        i_D = i_D + 1
    end
    -- etNew(1)
    -- etAim et=1 mode=0
    -- etSprite et=1 style=17 color=1
    -- etCountD et=1 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(1, 1, 5, 7)
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=1 speed=ecl_pick_rank(3.0, 3.0, 3.0, 5.0) step=ecl_pick_rank(1.2, 1.2, 1.2, 1.2)
    -- etEx et=1 params preserved
    -- etEx et=1 params preserved
    -- etOffsetAbs et=1 x=(-114) + ecl_var[-9997] y=(54) + ecl_var[-9996]
    liu_10_mc.bullet.ShotBulletMode(0, 1, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, ((-114) + ecl_var[-9997]) - self.x, ((54) + ecl_var[-9996]) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 1, 5, 7))), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(0.0), ecl_rad(0.0), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
    do return end
end
M.Boss4_at1e1 = ecl_Boss4_at1e1

function ecl_Boss4_at1e2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(2)
    -- etAim et=2 mode=1
    -- etSprite et=2 style=7 color=13
    -- etCount et=2 ways=1 layers=3
    -- etAngle et=2 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=2 speed=1.2 step=1.0
    -- etEx et=2 params preserved
    -- etEx et=2 params preserved
    -- etEx et=2 params preserved
    v_A = (ecl_var[-9989] + 3.1415927) + (0 / (16))
    i_D = 0
    i_E = 32
    for _ecl_loop = 1, math.max(0, math.floor(i_E)) do
        -- etOffsetAbs et=2 x=(114) + ecl_var[-9997] y=(54) + ecl_var[-9996]
        v_B = math.cos(v_A + 1.5707964) * (16.0)
        v_C = math.sin(v_A + 1.5707964) * (16.0)
        -- etOffset et=2 x=v_B y=v_C
        -- etAngle et=2 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        -- control-flow not structurally lowered: unless ((($D % 2) == 0) || ([-9959] >= 1)) goto Boss4_at1e2_1080 @ 0;
        liu_10_mc.bullet.ShotBulletMode(1, 2, _editor_class["ecl_stage06_boss_Bullet_7_13"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(3)), 1.2, 1.0, ecl_rad(v_A), ecl_rad(v_A), {{2, 1, 4, 60, -999999, 0.033333335, -999.0}})
        -- label Boss4_at1e2_1080
        v_A = v_A - 0.19635
        task._Wait(1)
        i_D = i_D + 1
    end
    -- etNew(2)
    -- etAim et=2 mode=0
    -- etSprite et=2 style=17 color=1
    -- etCountD et=2 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(1, 1, 5, 7)
    -- etAngle et=2 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=2 speed=ecl_pick_rank(3.0, 3.0, 3.0, 5.0) step=ecl_pick_rank(1.2, 1.2, 1.2, 1.2)
    -- etEx et=2 params preserved
    -- etEx et=2 params preserved
    -- etOffsetAbs et=2 x=(114) + ecl_var[-9997] y=(54) + ecl_var[-9996]
    liu_10_mc.bullet.ShotBulletMode(0, 2, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, ((114) + ecl_var[-9997]) - self.x, ((54) + ecl_var[-9996]) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 1, 5, 7))), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(0.0), ecl_rad(0.0), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
    do return end
end
M.Boss4_at1e2 = ecl_Boss4_at1e2

function ecl_Boss4_at1e3(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(3)
    -- etAim et=3 mode=1
    -- etSprite et=3 style=7 color=2
    -- etCount et=3 ways=1 layers=3
    -- etAngle et=3 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=3 speed=1.2 step=1.0
    -- etEx et=3 params preserved
    -- etEx et=3 params preserved
    -- etEx et=3 params preserved
    v_A = (ecl_var[-9989] - 1.5707964) + (0 / (16))
    i_D = 0
    i_E = 32
    for _ecl_loop = 1, math.max(0, math.floor(i_E)) do
        -- etOffsetAbs et=3 x=(-64) + ecl_var[-9997] y=(-80) + ecl_var[-9996]
        v_B = math.cos(v_A + 1.5707964) * (16.0)
        v_C = math.sin(v_A + 1.5707964) * (16.0)
        -- etOffset et=3 x=v_B y=v_C
        -- etAngle et=3 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        -- control-flow not structurally lowered: unless ((($D % 2) == 0) || ([-9959] >= 1)) goto Boss4_at1e3_1080 @ 0;
        liu_10_mc.bullet.ShotBulletMode(1, 3, _editor_class["ecl_stage06_boss_Bullet_7_2"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(3)), 1.2, 1.0, ecl_rad(v_A), ecl_rad(v_A), {{2, 1, 4, 60, -999999, 0.033333335, -999.0}})
        -- label Boss4_at1e3_1080
        v_A = v_A - 0.19635
        task._Wait(1)
        i_D = i_D + 1
    end
    -- etNew(3)
    -- etAim et=3 mode=0
    -- etSprite et=3 style=17 color=1
    -- etCountD et=3 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(1, 1, 5, 7)
    -- etAngle et=3 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=3 speed=ecl_pick_rank(3.0, 3.0, 3.0, 5.0) step=ecl_pick_rank(1.2, 1.2, 1.2, 1.2)
    -- etEx et=3 params preserved
    -- etEx et=3 params preserved
    -- etOffsetAbs et=3 x=(-64) + ecl_var[-9997] y=(-80) + ecl_var[-9996]
    liu_10_mc.bullet.ShotBulletMode(0, 3, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, ((-64) + ecl_var[-9997]) - self.x, ((-80) + ecl_var[-9996]) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 1, 5, 7))), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(0.0), ecl_rad(0.0), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
    do return end
end
M.Boss4_at1e3 = ecl_Boss4_at1e3

function ecl_Boss4_at1e4(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(4)
    -- etAim et=4 mode=1
    -- etSprite et=4 style=7 color=2
    -- etCount et=4 ways=1 layers=3
    -- etAngle et=4 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=4 speed=1.2 step=1.0
    -- etEx et=4 params preserved
    -- etEx et=4 params preserved
    -- etEx et=4 params preserved
    v_A = (ecl_var[-9989] + 1.5707964) + (0 / (16))
    i_D = 0
    i_E = 32
    for _ecl_loop = 1, math.max(0, math.floor(i_E)) do
        -- etOffsetAbs et=4 x=(64) + ecl_var[-9997] y=(-80) + ecl_var[-9996]
        v_B = math.cos(v_A + 1.5707964) * (16.0)
        v_C = math.sin(v_A + 1.5707964) * (16.0)
        -- etOffset et=4 x=v_B y=v_C
        -- etAngle et=4 angle=ecl_rad(v_A) step=ecl_rad(v_A)
        -- control-flow not structurally lowered: unless ((($D % 2) == 0) || ([-9959] >= 1)) goto Boss4_at1e4_1080 @ 0;
        liu_10_mc.bullet.ShotBulletMode(1, 4, _editor_class["ecl_stage06_boss_Bullet_7_2"], self.x, self.y, v_B, v_C, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(3)), 1.2, 1.0, ecl_rad(v_A), ecl_rad(v_A), {{2, 1, 4, 60, -999999, 0.033333335, -999.0}})
        -- label Boss4_at1e4_1080
        v_A = v_A + 0.19635
        task._Wait(1)
        i_D = i_D + 1
    end
    -- etNew(4)
    -- etAim et=4 mode=0
    -- etSprite et=4 style=17 color=1
    -- etCountD et=4 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(1, 1, 5, 7)
    -- etAngle et=4 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=4 speed=ecl_pick_rank(3.0, 3.0, 3.0, 5.0) step=ecl_pick_rank(1.2, 1.2, 1.2, 1.2)
    -- etEx et=4 params preserved
    -- etEx et=4 params preserved
    -- etOffsetAbs et=4 x=(64) + ecl_var[-9997] y=(-80) + ecl_var[-9996]
    liu_10_mc.bullet.ShotBulletMode(0, 4, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, ((64) + ecl_var[-9997]) - self.x, ((-80) + ecl_var[-9996]) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 1, 5, 7))), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(0.0), ecl_rad(0.0), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
    do return end
end
M.Boss4_at1e4 = ecl_Boss4_at1e4

function ecl_Boss5(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    self.hp, self.maxhp = 3000, 3000
    self.hp, self.maxhp = 1800, 1800
    self.hp, self.maxhp = 2200, 2200
    -- visual/helper ins_259(3, -1)
    -- visual/helper ins_259(4, -1)
    -- visual/helper ins_259(5, -1)
    -- visual/helper ins_259(6, -1)
    -- visual/helper ins_259(7, -1)
    -- visual/helper ins_259(8, -1)
    -- visual/helper ins_259(9, -1)
    -- visual/helper ins_259(10, -1)
    -- visual/helper ins_259(11, -1)
    -- visual/helper ins_259(12, -1)
    -- unsupported ins_402(2)
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss5_528 @ 0;
    -- unsupported ins_512(640.0f)
    -- control-flow not structurally lowered: goto Boss5_548 @ 0;
    -- label Boss5_528
    -- unsupported ins_513(640.0f)
    -- label Boss5_548
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    -- unsupported ins_405()
    -- boss/meta ins_427(0, 3000.0f, -24448)
    -- boss/meta ins_427(0, 1800.0f, -24448)
    -- boss/meta ins_427(0, 2200.0f, -24448)
    -- visual/helper ins_440(1)
    -- unsupported ins_415(130)
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss5_2176 @ 0;
    v_C = ecl_var[-9997]
    v_D = ecl_var[-9996]
    self.x, self.y = v_C + (-114), v_D + (54)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 10)
    -- unsupported ins_407(2, 13)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (114), v_D + (54)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 10)
    -- unsupported ins_407(2, 13)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (-64), v_D + (-80)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 10)
    -- unsupported ins_407(2, 13)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C + (64), v_D + (-80)
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 10)
    -- unsupported ins_407(2, 13)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    self.x, self.y = v_C, v_D
    ecl_sync_self(self)
    -- unsupported ins_406()
    -- unsupported ins_407(1, 20)
    -- unsupported ins_407(2, 25)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    -- label Boss5_2176
    -- visual/helper ins_416(28)
    task.MoveTo(0.0, 128.0, 60, 0)
    ecl_sync_self(self)
    task._Wait(120)
    SetV2(self, 112.0, 0.0, true, false)
    ecl_BossCard5(self)
    do return end
end
M.Boss5 = ecl_Boss5

function ecl_Boss6(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    self.hp, self.maxhp = 7000, 7000
    -- visual/helper ins_259(3, -1)
    -- visual/helper ins_259(4, -1)
    -- visual/helper ins_259(5, -1)
    -- visual/helper ins_259(6, -1)
    -- visual/helper ins_259(7, -1)
    -- visual/helper ins_259(8, -1)
    -- visual/helper ins_259(9, -1)
    -- visual/helper ins_259(10, -1)
    -- visual/helper ins_259(11, -1)
    -- visual/helper ins_259(12, -1)
    -- unsupported ins_402(2)
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss6_488 @ 0;
    -- unsupported ins_512(640.0f)
    -- control-flow not structurally lowered: goto Boss6_508 @ 0;
    -- label Boss6_488
    -- unsupported ins_513(640.0f)
    -- label Boss6_508
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    -- unsupported ins_405()
    -- boss/meta ins_427(0, 7000.0f, -24448)
    -- visual/helper ins_440(0)
    -- unsupported ins_415(130)
    -- control-flow not structurally lowered: unless ([-9986] == 0) goto Boss6_1036 @ 0;
    -- unsupported ins_406()
    -- unsupported ins_410(3)
    -- unsupported ins_407(1, 100)
    -- unsupported ins_407(2, 90)
    -- unsupported ins_408(64.0f, 64.0f)
    -- unsupported ins_409()
    -- label Boss6_1036
    -- visual/helper ins_416(28)
    task.MoveTo(0.0, 128.0, 60, 0)
    ecl_sync_self(self)
    task._Wait(120)
    SetV2(self, 112.0, 0.0, true, false)
    ecl_BossCard6(self)
    do return end
end
M.Boss6 = ecl_Boss6

function ecl_BossCard1(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- unsupported ins_256("Ecl_EtBreak", 0.0f, 0.0f, 9999, 0, 0)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    -- setInterrupt phase=0 life=0 time=2700 sub="Boss2"
    -- setInterrupt phase=0 life=0 time=2100 sub="Boss2"
    -- boss/meta ins_437(77, 2700, 500000, "���@�u���_�̃I�[�����v")
    -- boss/meta ins_439(79, 2700, 500000, "�g���u���̉_�H�v")
    -- boss/meta ins_422(80, 2700, 500000, "�g���u�Ɋy�̎��̉_�H�v")
    -- boss/meta ins_424(43)
    task.MoveTo(0.0, 160.0, 60, 4)
    ecl_sync_self(self)
    SetV2(self, 128.0, 0.0, true, false)
    -- visual/helper ins_262(0, 0)
    -- +60:
    -- visual/helper ins_263(0, 119)
    task._Wait(60)
    task.MoveTo(0.0, 128.0, 200, 4)
    ecl_sync_self(self)
    while true do
        -- visual/helper ins_269(0)
        task.New(self, function() ecl_BossCard1_at1(self) end)
        task.New(self, function() ecl_BossCard1_at2(self) end)
        task.New(self, function() ecl_BossCard1_at1h(self) end)
        task.New(self, function() ecl_BossCard1_at2h(self) end)
        task._Wait(230)
        task.New(self, _editor_tasks["liu_10_mc_moveRand"](60, 4, 3.0))
        task._Wait(70)
    end
    while true do
        task._Wait(1000)
    end
    do return end
end
M.BossCard1 = ecl_BossCard1

function ecl_BossCard1_at1(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etAim et=0 mode=3
    -- etSprite et=0 style=29 color=0
    -- etCountD et=0 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(2, 4, 4, 4)
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=0 speed=ecl_pick_rank(2.0, 2.2, 2.5, 2.5) step=ecl_pick_rank(1.2, 1.0, 1.0, 1.0)
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    v_A = 3.1415927 + (0 / (8))
    v_B = (80)
    i_C = 80
    for _ecl_loop = 1, math.max(0, math.floor(i_C)) do
        -- etDist et=0 distance=v_B
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.18479957)
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_29_0"], self.x, self.y, v_B, v_C, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(2, 4, 4, 4))), ecl_pick_rank(2.0, 2.2, 2.5, 2.5), ecl_pick_rank(1.2, 1.0, 1.0, 1.0), ecl_rad(v_A), ecl_rad(0.18479957), {{1, 0, 4, 60, -999999, 0.016666668, -999.0}})
        v_B = v_B - (1)
        v_A = v_A - 0.15708
        task._Wait(2)
    end
    i_D = 40
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etDist et=0 distance=v_B
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.18479957)
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_29_0"], self.x, self.y, v_B, v_C, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(2, 4, 4, 4))), ecl_pick_rank(2.0, 2.2, 2.5, 2.5), ecl_pick_rank(1.2, 1.0, 1.0, 1.0), ecl_rad(v_A), ecl_rad(0.18479957), {{1, 0, 4, 60, -999999, 0.016666668, -999.0}})
        v_B = v_B - (1)
        v_A = v_A - 0.15708
        task._Wait(1)
    end
    do return end
end
M.BossCard1_at1 = ecl_BossCard1_at1

function ecl_BossCard1_at1h(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etAim et=0 mode=3
    -- etSprite et=0 style=29 color=0
    -- etCountD et=0 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(2, 4, 4, 4)
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=0 speed=ecl_pick_rank(2.0, 2.5, 2.5, 2.5) step=ecl_pick_rank(1.2, 1.0, 1.0, 1.0)
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    v_A = 3.1415927 + (0 / (8))
    v_B = (80)
    i_C = 80
    for _ecl_loop = 1, math.max(0, math.floor(i_C)) do
        -- etDist et=0 distance=v_B
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.007853982)
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_29_0"], self.x, self.y, v_B, v_C, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(2, 4, 4, 4))), ecl_pick_rank(2.0, 2.5, 2.5, 2.5), ecl_pick_rank(1.2, 1.0, 1.0, 1.0), ecl_rad(v_A), ecl_rad(0.007853982), {{1, 0, 4, 60, -999999, 0.016666668, -999.0}})
        v_B = v_B - (1)
        v_A = v_A + 0.15708
        task._Wait(2)
    end
    i_D = 40
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etDist et=0 distance=v_B
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.007853982)
        liu_10_mc.bullet.ShotBulletMode(3, 0, _editor_class["ecl_stage06_boss_Bullet_29_0"], self.x, self.y, v_B, v_C, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(2, 4, 4, 4))), ecl_pick_rank(2.0, 2.5, 2.5, 2.5), ecl_pick_rank(1.2, 1.0, 1.0, 1.0), ecl_rad(v_A), ecl_rad(0.007853982), {{1, 0, 4, 60, -999999, 0.016666668, -999.0}})
        v_B = v_B - (1)
        v_A = v_A + 0.15708
        task._Wait(1)
    end
    do return end
end
M.BossCard1_at1h = ecl_BossCard1_at1h

function ecl_BossCard1_at2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(1)
    -- etAim et=1 mode=3
    -- etSprite et=1 style=28 color=4
    -- etCountD et=1 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(2, 4, 4, 4)
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=1 speed=ecl_pick_rank(1.3, 1.3, 1.6, 1.6) step=ecl_pick_rank(0.6, 0.5, 0.5, 0.5)
    -- etEx et=1 params preserved
    v_A = -1.5707964 + (0 / (8))
    v_B = (80)
    i_C = 40
    for _ecl_loop = 1, math.max(0, math.floor(i_C)) do
        -- etDist et=1 distance=v_B
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(0.14279966)
        liu_10_mc.bullet.ShotBulletMode(3, 1, _editor_class["ecl_stage06_boss_Bullet_28_4"], self.x, self.y, ((-114) + ecl_var[-9997]) - self.x, ((54) + ecl_var[-9996]) - self.y, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(2, 4, 4, 4))), ecl_pick_rank(1.3, 1.3, 1.6, 1.6), ecl_pick_rank(0.6, 0.5, 0.5, 0.5), ecl_rad(v_A), ecl_rad(0.14279966), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        v_B = v_B - (1)
        v_A = v_A - 0.15708
        task._Wait(2)
    end
    i_D = 40
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etDist et=1 distance=v_B
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(0.1308997)
        liu_10_mc.bullet.ShotBulletMode(3, 1, _editor_class["ecl_stage06_boss_Bullet_28_4"], self.x, self.y, ((-114) + ecl_var[-9997]) - self.x, ((54) + ecl_var[-9996]) - self.y, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(2, 4, 4, 4))), ecl_pick_rank(1.3, 1.3, 1.6, 1.6), ecl_pick_rank(0.6, 0.5, 0.5, 0.5), ecl_rad(v_A), ecl_rad(0.1308997), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        v_B = v_B - (1)
        v_A = v_A + 0.15708
        task._Wait(1)
    end
    do return end
end
M.BossCard1_at2 = ecl_BossCard1_at2

function ecl_BossCard1_at2h(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(1)
    -- etAim et=1 mode=3
    -- etSprite et=1 style=28 color=4
    -- etCountD et=1 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(2, 4, 4, 4)
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeedD et=1 speed=ecl_pick_rank(1.3, 1.6, 1.6, 1.6) step=ecl_pick_rank(0.6, 0.5, 0.5, 0.5)
    -- etEx et=1 params preserved
    v_A = -1.5707964 + (0 / (8))
    v_B = (80)
    i_C = 40
    for _ecl_loop = 1, math.max(0, math.floor(i_C)) do
        -- etDist et=1 distance=v_B
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(0.14279966)
        liu_10_mc.bullet.ShotBulletMode(3, 1, _editor_class["ecl_stage06_boss_Bullet_28_4"], self.x, self.y, ((-114) + ecl_var[-9997]) - self.x, ((54) + ecl_var[-9996]) - self.y, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(2, 4, 4, 4))), ecl_pick_rank(1.3, 1.6, 1.6, 1.6), ecl_pick_rank(0.6, 0.5, 0.5, 0.5), ecl_rad(v_A), ecl_rad(0.14279966), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        v_B = v_B - (1)
        v_A = v_A + 0.15708
        task._Wait(2)
    end
    i_D = 40
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etDist et=1 distance=v_B
        -- etAngle et=1 angle=ecl_rad(v_A) step=ecl_rad(0.1308997)
        liu_10_mc.bullet.ShotBulletMode(3, 1, _editor_class["ecl_stage06_boss_Bullet_28_4"], self.x, self.y, ((-114) + ecl_var[-9997]) - self.x, ((54) + ecl_var[-9996]) - self.y, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(2, 4, 4, 4))), ecl_pick_rank(1.3, 1.6, 1.6, 1.6), ecl_pick_rank(0.6, 0.5, 0.5, 0.5), ecl_rad(v_A), ecl_rad(0.1308997), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        v_B = v_B - (1)
        v_A = v_A - 0.15708
        task._Wait(1)
    end
    do return end
end
M.BossCard1_at2h = ecl_BossCard1_at2h

function ecl_BossCard2(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- unsupported ins_256("Ecl_EtBreak", 0.0f, 0.0f, 9999, 0, 0)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    -- setInterrupt phase=0 life=0 time=2700 sub="Boss3"
    -- boss/meta ins_437(81, 2700, 500000, "���@�u���E���̗d���v")
    -- boss/meta ins_439(83, 2700, 500000, "���@�u�}�W�b�N�o�^�t���C�v")
    task.MoveTo(0.0, 192.0, 60, 4)
    ecl_sync_self(self)
    -- unsupported ins_415(60)
    -- boss/meta ins_424(44)
    -- unsupported ins_405()
    -- visual/helper ins_263(0, 119)
    -- +60:
    -- visual/helper ins_269(0)
    -- +30:
    -- unsupported ins_0()
    task.New(self, function() ecl_BossEyes2(self) end)
    while true do
        -- unsupported ins_448(200, 100, 100, 90)
        ecl_BossCard2_at2(self)
        task._Wait(1)
    end
    while true do
        task._Wait(1000)
    end
    do return end
end
M.BossCard2 = ecl_BossCard2

function ecl_BossCard2_at1(self, v_A, v_B, v_C)
    ecl_sync_self(self)
    local i_A = v_A or 0
    local i_B = v_B or 0
    local i_C = v_C or 0
    -- etNew(0)
    -- etAim et=0 mode=1
    -- etSprite et=0 style=21 color=3
    -- etCountD et=0 ways=ecl_pick_rank(1, 1, 1, 1) layers=ecl_pick_rank(1, 3, 3, 3)
    -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.28559932)
    -- etSpeedD et=0 speed=ecl_pick_rank(2.0, 2.0, 2.8, 2.8) step=ecl_pick_rank(1.0, 1.0, 1.0, 1.0)
    -- etEx et=0 params preserved
    -- etDist et=0 distance=16.0
    -- etOffsetAbs et=0 x=v_B y=v_C
    liu_10_mc.bullet.ShotBulletMode(1, 0, _editor_class["ecl_stage06_boss_Bullet_21_3"], self.x, self.y, (v_B) - self.x, (v_C) - self.y, 16.0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 3, 3, 3))), ecl_pick_rank(2.0, 2.0, 2.8, 2.8), ecl_pick_rank(1.0, 1.0, 1.0, 1.0), ecl_rad(v_A), ecl_rad(0.28559932), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
    do return end
end
M.BossCard2_at1 = ecl_BossCard2_at1

function ecl_BossCard2_at2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etSprite et=0 style=7 color=4
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.0)
    -- etSpeed et=0 speed=8.0 step=8.0
    -- laser ins_600(0, 0.0f, 512.0f, 16.0f, 16.0f) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- laser ins_601(0, 60, 16, 30, 15, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- unsupported ins_508(0, 19, -1)
    v_A = ecl_var[-9989]
    i_D = 16
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        -- laser ins_603(0, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
        v_A = v_A + 0.392699
    end
    do return end
end
M.BossCard2_at2 = ecl_BossCard2_at2

function ecl_BossCard3(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- unsupported ins_256("Ecl_EtBreak", 0.0f, 0.0f, 9999, 0, 0)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    task.New(self, function() ecl_BossEyes(self) end)
    -- setInterrupt phase=0 life=0 time=3000 sub="Boss4"
    -- boss/meta ins_437(85, 3000, 500000, "�����u�X�^�[���C���V���g�����v")
    -- boss/meta ins_439(87, 3000, 500000, "�����u���@��͌n�v")
    -- boss/meta ins_422(88, 3000, 500000, "�����u���@��͌n�v")
    task.MoveTo(0.0, 192.0, 60, 4)
    ecl_sync_self(self)
    -- unsupported ins_415(60)
    -- boss/meta ins_424(44)
    -- unsupported ins_405()
    -- +60:
    -- visual/helper ins_263(0, 119)
    -- +60:
    -- visual/helper ins_269(0)
    task.New(self, function() ecl_BossCard3_at(self) end)
    task.New(self, function() ecl_BossCard3_at2(self) end)
    task.New(self, function() ecl_BossCard3_at2b(self) end)
    while true do
        task._Wait(160)
    end
    do return end
end
M.BossCard3 = ecl_BossCard3

function ecl_BossCard3_at(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    task._Wait(300)
    -- etNew(2)
    -- etAim et=2 mode=0
    -- etSprite et=2 style=15 color=6
    -- etCount et=2 ways=1 layers=1
    -- etAngle et=2 angle=ecl_rad(0.0) step=ecl_rad(0.28559932)
    -- etSpeed et=2 speed=2.5 step=1.0
    -- etEx et=2 params preserved
    -- unsupported ins_511(3, 2)
    -- unsupported ins_511(4, 2)
    -- unsupported ins_511(5, 2)
    -- etOffsetAbs et=2 x=ecl_var[-9997] + (-114) y=ecl_var[-9996] + (54)
    -- etOffsetAbs et=3 x=ecl_var[-9997] + (114) y=ecl_var[-9996] + (54)
    -- etOffsetAbs et=4 x=ecl_var[-9997] + (-64) y=ecl_var[-9996] + (-80)
    -- etOffsetAbs et=5 x=ecl_var[-9997] + (64) y=ecl_var[-9996] + (-80)
    -- unsupported ins_435($A, 200, 200, 200, 100)
    while true do
        liu_10_mc.bullet.ShotBulletMode(0, 2, _editor_class["ecl_stage06_boss_Bullet_15_6"], self.x, self.y, (ecl_var[-9997] + (-114)) - self.x, (ecl_var[-9996] + (54)) - self.y, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), 2.5, 1.0, ecl_rad(0.0), ecl_rad(0.28559932), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(0, 3, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, (ecl_var[-9997] + (114)) - self.x, (ecl_var[-9996] + (54)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 1, 5, 7))), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(0.0), ecl_rad(0.0), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(0, 4, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, (ecl_var[-9997] + (-64)) - self.x, (ecl_var[-9996] + (-80)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 1, 5, 7))), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(0.0), ecl_rad(0.0), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(3, 5, _editor_class["ecl_stage06_boss_Bullet_1_0"], self.x, self.y, (ecl_var[-9997] + (64)) - self.x, (ecl_var[-9996] + (-80)) - self.y, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), 1.0, 0.0, 0, 0, nil)
        task._Wait(i_A)
        -- control-flow not structurally lowered: unless ($A >= 60) goto BossCard3_at_1208 @ 0;
        i_A = i_A - 5
    end
    do return end
end
M.BossCard3_at = ecl_BossCard3_at

function ecl_BossCard3_at2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E, v_F, i_F, v_G, i_G, v_H, i_H = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etSprite et=0 style=0 color=13
    -- etAngle et=0 angle=ecl_rad(-0.7853982) step=ecl_rad(-0.7853982)
    -- etSpeed et=0 speed=4.0 step=4.0
    -- laser ins_600(0, -1.0f, -1.0f, -1.0f, 16.0f) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- laser ins_601(0, 32, -1, -1, -1, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- unsupported ins_508(0, 19, -1)
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    v_A = 2.356194
    -- unsupported ins_436(%E, 128.0f, 64.0f, 64.0f, 64.0f)
    v_B = (240)
    v_C = (448)
    i_F = 10000
    for _ecl_loop = 1, math.max(0, math.floor(i_F)) do
        v_D = (-32)
        i_G = 4
        for _ecl_loop = 1, math.max(0, math.floor(i_G)) do
            v_C = (ecl_var[-9999] * v_E) + v_D
            -- etOffsetAbs et=0 x=v_B y=v_C
            -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
            -- laser ins_611(0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
            -- unsupported ins_448(14, 14, 12, 10)
            v_D = v_D + v_E
            v_D = v_D + v_E
        end
        -- control-flow not structurally lowered: unless ([-9959] >= 1) goto BossCard3_at2_1764 @ 0;
        v_D = (-32) + v_E
        i_H = 4
        for _ecl_loop = 1, math.max(0, math.floor(i_H)) do
            v_C = (ecl_var[-9999] * v_E) + v_D
            -- etOffsetAbs et=0 x=v_B y=v_C
            -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
            -- laser ins_611(0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
            -- unsupported ins_448(14, 14, 12, 10)
            v_D = v_D + v_E
            v_D = v_D + v_E
        end
    end
    do return end
end
M.BossCard3_at2 = ecl_BossCard3_at2

function ecl_BossCard3_at2b(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E, v_F, i_F, v_G, i_G, v_H, i_H = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(0)
    -- etSprite et=0 style=0 color=13
    -- etAngle et=0 angle=ecl_rad(-0.7853982) step=ecl_rad(-0.7853982)
    -- etSpeed et=0 speed=4.0 step=4.0
    -- laser ins_600(0, -1.0f, -1.0f, -1.0f, 16.0f) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- laser ins_601(0, 32, -1, -1, -1, 0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
    -- unsupported ins_508(0, 19, -1)
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    v_A = -0.785398
    -- unsupported ins_436(%E, 128.0f, 64.0f, 64.0f, 64.0f)
    v_B = (-240)
    task._Wait(40)
    i_F = 10000
    for _ecl_loop = 1, math.max(0, math.floor(i_F)) do
        v_D = (0)
        i_G = 4
        for _ecl_loop = 1, math.max(0, math.floor(i_G)) do
            v_C = (ecl_var[-9999] * v_E) + v_D
            -- etOffsetAbs et=0 x=v_B y=v_C
            -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
            -- laser ins_611(0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
            -- unsupported ins_448(14, 14, 12, 10)
            v_D = v_D + v_E
            v_D = v_D + v_E
        end
        -- control-flow not structurally lowered: unless ([-9959] >= 1) goto BossCard3_at2b_1744 @ 0;
        v_D = (-32) + v_E
        i_H = 4
        for _ecl_loop = 1, math.max(0, math.floor(i_H)) do
            v_C = (ecl_var[-9999] * v_E) + v_D
            -- etOffsetAbs et=0 x=v_B y=v_C
            -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
            -- laser ins_611(0) TODO: map to liu_10_mc.bullet.LineLaser/InfLaser
            -- unsupported ins_448(14, 14, 12, 10)
            v_D = v_D + v_E
            v_D = v_D + v_E
        end
    end
    do return end
end
M.BossCard3_at2b = ecl_BossCard3_at2b

function ecl_BossCard4(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- unsupported ins_256("Ecl_EtBreak", 0.0f, 0.0f, 9999, 0, 0)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    task.New(self, function() ecl_BossEyes(self) end)
    -- setInterrupt phase=0 life=0 time=4200 sub="Boss6"
    -- setInterrupt phase=0 life=0 time=4200 sub="Boss5"
    -- boss/meta ins_437(89, 4200, 500000, "�喂�@�u���_���u�v")
    -- boss/meta ins_439(91, 4200, 500000, "�喂�@�u���_���u�v")
    -- boss/meta ins_422(92, 4200, 500000, "�喂�@�u���_���u�v")
    task.MoveTo(0.0, 224.0, 60, 4)
    ecl_sync_self(self)
    -- unsupported ins_415(60)
    -- boss/meta ins_424(44)
    -- unsupported ins_405()
    -- +60:
    -- visual/helper ins_263(0, 119)
    -- +60:
    -- visual/helper ins_269(0)
    -- unsupported ins_417(120, 0, 1)
    -- visual/helper ins_416(58)
    ecl_var[-9982] = 69
    ecl_var[-9981] = 1.570796
    ecl_var[-9980] = (-114)
    ecl_var[-9979] = (54)
    -- unsupported ins_256("BossCard4Laser", -114.0f, 54.0f, 100, 10, 0)
    ecl_var[-9980] = (114)
    ecl_var[-9979] = (54)
    -- unsupported ins_256("BossCard4Laser", 114.0f, 54.0f, 100, 10, 0)
    ecl_var[-9980] = (-64)
    ecl_var[-9979] = (-80)
    -- unsupported ins_256("BossCard4Laser", -64.0f, -80.0f, 100, 10, 0)
    ecl_var[-9980] = (64)
    ecl_var[-9979] = (-80)
    -- unsupported ins_256("BossCard4Laser", 64.0f, -80.0f, 100, 10, 0)
    task._Wait(120)
    -- visual/helper ins_416(52)
    -- unsupported ins_417(60, 4, 0)
    task.MoveTo(0.0, 128.0, 60, 4)
    ecl_sync_self(self)
    task.New(self, function() ecl_BossCard4_at(self) end)
    task.New(self, function() ecl_BossCard4_at2(self) end)
    task.New(self, function() ecl_BossCard4_at3(self) end)
    task.New(self, function() ecl_BossCard4_at4(self) end)
    task.New(self, function() ecl_BossCard4_at5(self) end)
    task.New(self, function() ecl_BossCard4_at6(self) end)
    task.New(self, function() ecl_BossCard4_at7(self) end)
    while true do
        task._Wait(160)
    end
    do return end
end
M.BossCard4 = ecl_BossCard4

function ecl_BossCard4_at(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- etNew(2)
    -- etAim et=2 mode=1
    -- etSprite et=2 style=11 color=6
    -- etCount et=2 ways=2 layers=1
    -- etAngle et=2 angle=ecl_rad(0.0) step=ecl_rad(0.28559932)
    -- etSpeed et=2 speed=6.5 step=1.0
    -- etEx et=2 params preserved
    -- unsupported ins_511(3, 2)
    -- unsupported ins_511(4, 2)
    -- unsupported ins_511(5, 2)
    v_A = 1.570796
    v_B = 1.570796
    v_C = 6.283185
    i_D = 50
    for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
        -- etOffsetAbs et=2 x=ecl_var[-9997] + (-114) y=ecl_var[-9996] + (54)
        -- etOffsetAbs et=3 x=ecl_var[-9997] + (114) y=ecl_var[-9996] + (54)
        -- etOffsetAbs et=4 x=ecl_var[-9997] + (-64) y=ecl_var[-9996] + (-80)
        -- etOffsetAbs et=5 x=ecl_var[-9997] + (64) y=ecl_var[-9996] + (-80)
        -- etAngle et=2 angle=ecl_rad(v_A) step=ecl_rad(v_C)
        -- etAngle et=4 angle=ecl_rad(v_A) step=ecl_rad(v_C)
        -- etAngle et=3 angle=ecl_rad(v_B) step=ecl_rad(v_C)
        -- etAngle et=5 angle=ecl_rad(v_B) step=ecl_rad(v_C)
        v_C = v_C - 0.083776
        liu_10_mc.bullet.ShotBulletMode(1, 2, _editor_class["ecl_stage06_boss_Bullet_11_6"], self.x, self.y, (ecl_var[-9997] + (-114)) - self.x, (ecl_var[-9996] + (54)) - self.y, 0, 0, 0, math.max(1, math.floor(2)), math.max(1, math.floor(1)), 6.5, 1.0, ecl_rad(v_A), ecl_rad(v_C), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(0, 3, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, (ecl_var[-9997] + (114)) - self.x, (ecl_var[-9996] + (54)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 1, 5, 7))), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(v_B), ecl_rad(v_C), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(0, 4, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, (ecl_var[-9997] + (-64)) - self.x, (ecl_var[-9996] + (-80)) - self.y, 0, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), math.max(1, math.floor(ecl_pick_rank(1, 1, 5, 7))), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(v_A), ecl_rad(v_C), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(3, 5, _editor_class["ecl_stage06_boss_Bullet_1_0"], self.x, self.y, (ecl_var[-9997] + (64)) - self.x, (ecl_var[-9996] + (-80)) - self.y, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), 1.0, 0.0, ecl_rad(v_B), ecl_rad(v_C), nil)
        task._Wait(3)
    end
    i_E = 0
    -- etCount et=2 ways=3 layers=1
    -- etCount et=3 ways=3 layers=1
    -- etCount et=4 ways=3 layers=1
    -- etCount et=5 ways=3 layers=1
    v_C = 0.010472
    while true do
        -- etOffsetAbs et=2 x=ecl_var[-9997] + (-114) y=ecl_var[-9996] + (54)
        -- etOffsetAbs et=3 x=ecl_var[-9997] + (114) y=ecl_var[-9996] + (54)
        -- etOffsetAbs et=4 x=ecl_var[-9997] + (-64) y=ecl_var[-9996] + (-80)
        -- etOffsetAbs et=5 x=ecl_var[-9997] + (64) y=ecl_var[-9996] + (-80)
        -- etAngle et=2 angle=ecl_rad(v_A) step=ecl_rad(1.0471976)
        -- etAngle et=5 angle=ecl_rad(v_A) step=ecl_rad(1.0471976)
        -- etAngle et=3 angle=ecl_rad(v_B) step=ecl_rad(1.0471976)
        -- etAngle et=4 angle=ecl_rad(v_B) step=ecl_rad(1.0471976)
        -- control-flow not structurally lowered: unless ($E == 0) goto BossCard4_at_2724 @ 0;
        v_A = v_A - v_C
        v_B = v_B + v_C
        -- control-flow not structurally lowered: unless (%A < (1.5707964f - (3.1415927f / _f(9)))) goto BossCard4_at_2700 @ 0;
        i_E = 1
        -- label BossCard4_at_2700
        -- control-flow not structurally lowered: goto BossCard4_at_3068 @ 0;
        -- label BossCard4_at_2724
        v_A = v_A + v_C
        v_B = v_B - v_C
        -- control-flow not structurally lowered: unless (%A > (1.5707964f + (3.1415927f / _f(28)))) goto BossCard4_at_3068 @ 0;
        i_E = 0
        -- label BossCard4_at_3068
        liu_10_mc.bullet.ShotBulletMode(1, 2, _editor_class["ecl_stage06_boss_Bullet_11_6"], self.x, self.y, (ecl_var[-9997] + (-114)) - self.x, (ecl_var[-9996] + (54)) - self.y, 0, 0, 0, math.max(1, math.floor(3)), math.max(1, math.floor(1)), 6.5, 1.0, ecl_rad(v_A), ecl_rad(1.0471976), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(0, 3, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, (ecl_var[-9997] + (114)) - self.x, (ecl_var[-9996] + (54)) - self.y, 0, 0, 0, math.max(1, math.floor(3)), math.max(1, math.floor(1)), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(v_B), ecl_rad(1.0471976), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(0, 4, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, (ecl_var[-9997] + (-64)) - self.x, (ecl_var[-9996] + (-80)) - self.y, 0, 0, 0, math.max(1, math.floor(3)), math.max(1, math.floor(1)), ecl_pick_rank(3.0, 3.0, 3.0, 5.0), ecl_pick_rank(1.2, 1.2, 1.2, 1.2), ecl_rad(v_B), ecl_rad(1.0471976), {{1, 0, 1024, 100, 0, -999999.0, -999999.0}})
        liu_10_mc.bullet.ShotBulletMode(3, 5, _editor_class["ecl_stage06_boss_Bullet_1_0"], self.x, self.y, (ecl_var[-9997] + (64)) - self.x, (ecl_var[-9996] + (-80)) - self.y, 0, 0, 0, math.max(1, math.floor(3)), math.max(1, math.floor(1)), 1.0, 0.0, ecl_rad(v_A), ecl_rad(1.0471976), nil)
        task._Wait(3)
    end
    do return end
end
M.BossCard4_at = ecl_BossCard4_at

function ecl_BossCard4_at2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D = 0, 0, 0, 0, 0, 0, 0, 0
    ecl_HPWait(self, 3000, 2400)
    task._Wait(120)
    -- visual/helper ins_416(28)
    -- etNew(0)
    -- etAim et=0 mode=1
    -- etSprite et=0 style=17 color=2
    -- etCount et=0 ways=1 layers=1
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.28559932)
    -- etSpeed et=0 speed=2.5 step=1.0
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    -- unsupported ins_436(%B, 0.033333335f, 0.033333335f, 0.041666668f, 0.05f)
    -- etEx et=0 params preserved
    while true do
        v_A = 3.141593
        -- unsupported ins_435($C, 2, 6, 7, 8)
        for _ecl_loop = 1, math.max(0, math.floor(i_C)) do
            -- etEx et=0 params preserved
            -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
            liu_10_mc.bullet.ShotBulletMode(1, 0, _editor_class["ecl_stage06_boss_Bullet_17_2"], self.x, self.y, (v_B) - self.x, (v_C) - self.y, 16.0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), 2.5, 1.0, ecl_rad(v_A), ecl_rad(0.0), {{3, 0, 32, 1, 1, 0 / (16), ecl_var[-9999] * 1.0}})
            v_A = v_A + 3.141593
            v_A = v_A + 0.628319
            v_A = v_A + 0.523599
            v_A = v_A + 0.448799
            task._Wait(5)
        end
        -- control-flow not structurally lowered: unless ([-9964.0f] >= [-9996.0f]) goto BossCard4_at2_1304 @ 0;
        task._Wait(120)
        -- label BossCard4_at2_1304
        v_A = 0.0
        -- unsupported ins_435($D, 2, 6, 7, 8)
        for _ecl_loop = 1, math.max(0, math.floor(i_D)) do
            -- etEx et=0 params preserved
            -- etAngle et=0 angle=ecl_rad(v_A) step=ecl_rad(0.0)
            liu_10_mc.bullet.ShotBulletMode(1, 0, _editor_class["ecl_stage06_boss_Bullet_17_2"], self.x, self.y, (v_B) - self.x, (v_C) - self.y, 16.0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), 2.5, 1.0, ecl_rad(v_A), ecl_rad(0.0), {{3, 0, 32, 1, 1, 0 / (16), ecl_var[-9999] * 1.0}})
            v_A = v_A - 3.141593
            v_A = v_A - 0.628319
            v_A = v_A - 0.523599
            v_A = v_A - 0.448799
            task._Wait(5)
        end
        -- control-flow not structurally lowered: unless ([-9964.0f] >= [-9996.0f]) goto BossCard4_at2_2080 @ 0;
        task._Wait(120)
    end
    do return end
end
M.BossCard4_at2 = ecl_BossCard4_at2

function ecl_BossCard4_at3(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    ecl_HPWait(self, 4000, 2400)
    -- visual/helper ins_416(28)
    -- etNew(1)
    -- etAim et=1 mode=0
    -- etSprite et=1 style=26 color=0
    -- etCountD et=1 ways=ecl_pick_rank(1, 1, 3, 3) layers=ecl_pick_rank(1, 1, 1, 1)
    -- etAngle et=1 angle=ecl_rad(0.0) step=ecl_rad(0.7853982)
    -- etSpeedD et=1 speed=ecl_pick_rank(2.0, 2.0, 2.5, 3.0) step=ecl_pick_rank(1.0, 1.0, 1.0, 1.0)
    -- etEx et=1 params preserved
    while true do
        liu_10_mc.bullet.ShotBulletMode(0, 1, _editor_class["ecl_stage06_boss_Bullet_26_0"], self.x, self.y, ((-114) + ecl_var[-9997]) - self.x, ((54) + ecl_var[-9996]) - self.y, v_B, 0, 0, math.max(1, math.floor(ecl_pick_rank(1, 1, 3, 3))), math.max(1, math.floor(ecl_pick_rank(1, 1, 1, 1))), ecl_pick_rank(2.0, 2.0, 2.5, 3.0), ecl_pick_rank(1.0, 1.0, 1.0, 1.0), ecl_rad(0.0), ecl_rad(0.7853982), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        -- unsupported ins_448(240, 120, 100, 60)
        task._Wait(1)
    end
    do return end
end
M.BossCard4_at3 = ecl_BossCard4_at3

function ecl_BossCard4_at4(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    ecl_HPWait(self, 2000, 2400)
    -- visual/helper ins_416(28)
    while true do
        -- visual/helper ins_416(58)
        ecl_var[-9982] = 69
        ecl_var[-9981] = 1.570796
        ecl_var[-9980] = (-114)
        ecl_var[-9979] = (54)
        ecl_var[-9978] = 0.001164
        ecl_var[-9985] = 0
        -- unsupported ins_256("BossCard4Laser2", -114.0f, 54.0f, 100, 10, 0)
        ecl_var[-9980] = (114)
        ecl_var[-9979] = (54)
        ecl_var[-9985] = 1
        -- unsupported ins_256("BossCard4Laser2", 114.0f, 54.0f, 100, 10, 0)
        ecl_var[-9980] = (-64)
        ecl_var[-9979] = (-80)
        ecl_var[-9985] = 1
        -- unsupported ins_256("BossCard4Laser2", -64.0f, -80.0f, 100, 10, 0)
        ecl_var[-9980] = (64)
        ecl_var[-9979] = (-80)
        ecl_var[-9985] = 0
        -- unsupported ins_256("BossCard4Laser2", 64.0f, -80.0f, 100, 10, 0)
        task._Wait(32000)
    end
    do return end
end
M.BossCard4_at4 = ecl_BossCard4_at4

function ecl_BossCard4_at5(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B = 0, 0, 0, 0
    i_B = 0
    ecl_HPWait(self, 1000, 2400)
    -- visual/helper ins_416(28)
    -- etNew(6)
    -- etAim et=6 mode=0
    -- etSprite et=6 style=17 color=3
    -- etCount et=6 ways=1 layers=1
    -- etAngle et=6 angle=ecl_rad(0.0) step=ecl_rad(0.62831855)
    -- etSpeed et=6 speed=2.5 step=1.0
    -- etEx et=6 params preserved
    -- etEx et=6 params preserved
    v_A = -1.570796
    while true do
        -- etAngle et=6 angle=ecl_rad(v_A) step=ecl_rad(0.0)
        -- control-flow not structurally lowered: unless ($B == 0) goto BossCard4_at5_936 @ 0;
        v_A = v_A + 0.15708
        v_A = v_A + 0.20944
        v_A = v_A + 0.15708
        -- control-flow not structurally lowered: unless (%A >= 1.5707964f) goto BossCard4_at5_912 @ 0;
        i_B = 1
        -- label BossCard4_at5_912
        -- control-flow not structurally lowered: goto BossCard4_at5_1284 @ 0;
        -- label BossCard4_at5_936
        v_A = v_A - 0.15708
        v_A = v_A - 0.20944
        v_A = v_A - 0.15708
        -- control-flow not structurally lowered: unless (%A <= -1.5707964f) goto BossCard4_at5_1284 @ 0;
        i_B = 0
        -- label BossCard4_at5_1284
        liu_10_mc.bullet.ShotBulletMode(0, 6, _editor_class["ecl_stage06_boss_Bullet_17_3"], self.x, self.y, 0, 0, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), 2.5, 1.0, ecl_rad(v_A), ecl_rad(0.0), {{1, 0, 268435456, 1, -999999, -999999.0, -999999.0}})
        -- unsupported ins_448(6, 4, 2, 2)
        task._Wait(1)
    end
    do return end
end
M.BossCard4_at5 = ecl_BossCard4_at5

function ecl_BossCard4_at6(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    ecl_HPWait(self, -1, 3000)
    -- visual/helper ins_416(28)
    while true do
        -- etNew(7)
        -- etAim et=7 mode=2
        -- etSprite et=7 style=3 color=1
        -- etCount et=7 ways=16 layers=1
        -- etAngle et=7 angle=ecl_rad(0) step=ecl_rad(0.28559932)
        -- etSpeed et=7 speed=3.0 step=1.0
        -- etEx et=7 params preserved
        liu_10_mc.bullet.ShotBulletMode(3, 7, _editor_class["ecl_stage06_boss_Bullet_3_1"], self.x, self.y, 0, 0, 0, 0, 0, math.max(1, math.floor(16)), math.max(1, math.floor(1)), 3.0, 1.0, ecl_rad(0), ecl_rad(0.28559932), {{0, 1, 2, 1, -999999, -999999.0, -999999.0}})
        task._Wait(20)
    end
    do return end
end
M.BossCard4_at6 = ecl_BossCard4_at6

function ecl_BossCard4_at7(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C = 0, 0, 0, 0, 0, 0
    ecl_HPWait(self, -1, 200)
    -- etNew(7)
    -- etAim et=7 mode=2
    -- etSprite et=7 style=3 color=1
    -- etCount et=7 ways=16 layers=1
    -- etAngle et=7 angle=ecl_rad(0.0) step=ecl_rad(0.28559932)
    -- etSpeed et=7 speed=3.0 step=1.0
    -- etEx et=7 params preserved
    while true do
        -- etNew(7)
        -- etAim et=7 mode=1
        -- etSprite et=7 style=17 color=1
        -- etCount et=7 ways=1 layers=1
        -- etAngle et=7 angle=ecl_rad(1.5707964) step=ecl_rad(0.28559932)
        -- etSpeed et=7 speed=(ecl_var[-9999] * 2.0) + 0.5 step=1.0
        -- etEx et=7 params preserved
        -- etEx et=7 params preserved
        v_B = (ecl_var[-9999] * (128)) + (64)
        -- etSpeed et=7 speed=(v_B / 64.0) + (ecl_var[-9999] * 0.5) step=0.0
        -- etOffsetAbs et=7 x=v_B y=ecl_var[-9999] * (192)
        liu_10_mc.bullet.ShotBulletMode(1, 7, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, (v_B) - self.x, (ecl_var[-9999] * (192)) - self.y, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), (v_B / 64.0) + (ecl_var[-9999] * 0.5), 0.0, ecl_rad(1.5707964), ecl_rad(0.28559932), {{1, 0, 268435456, 1, -999999, -999999.0, -999999.0}})
        task._Wait(10)
        -- etNew(7)
        -- etAim et=7 mode=1
        -- etSprite et=7 style=17 color=1
        -- etCount et=7 ways=1 layers=1
        -- etAngle et=7 angle=ecl_rad(1.5707964) step=ecl_rad(0.28559932)
        -- etSpeed et=7 speed=(ecl_var[-9999] * 2.0) + 0.5 step=1.0
        -- etEx et=7 params preserved
        -- etEx et=7 params preserved
        v_B = (ecl_var[-9999] * (128)) + (64)
        -- etSpeed et=7 speed=(v_B / 64.0) + (ecl_var[-9999] * 0.5) step=0.0
        v_B = v_B * (-1)
        -- etOffsetAbs et=7 x=v_B y=ecl_var[-9999] * (192)
        liu_10_mc.bullet.ShotBulletMode(1, 7, _editor_class["ecl_stage06_boss_Bullet_17_1"], self.x, self.y, (v_B) - self.x, (ecl_var[-9999] * (192)) - self.y, 0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), (v_B / 64.0) + (ecl_var[-9999] * 0.5), 0.0, ecl_rad(1.5707964), ecl_rad(0.28559932), {{1, 0, 268435456, 1, -999999, -999999.0, -999999.0}})
        task._Wait(10)
    end
    do return end
end
M.BossCard4_at7 = ecl_BossCard4_at7

function ecl_BossCard5(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E, v_F, i_F, v_G, i_G, v_H, i_H, v_I, i_I, v_J, i_J = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- unsupported ins_256("Ecl_EtBreak", 0.0f, 0.0f, 9999, 0, 0)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    -- boss/meta ins_424(44)
    task.MoveTo(160.0, 128.0, 120, 4)
    ecl_sync_self(self)
    -- setInterrupt phase=0 life=0 time=4800 sub="Boss6"
    -- boss/meta ins_438(93, 4800, 500000, "�u������̃G�A�����v")
    -- boss/meta ins_439(94, 4800, 500000, "�u������̃G�A�����v")
    -- boss/meta ins_422(95, 4800, 500000, "���l�u�����@�v")
    -- unsupported ins_415(70)
    -- unsupported ins_405()
    v_B = (32)
    task._Wait(60)
    while true do
        -- visual/helper ins_263(0, 119)
        -- visual/helper ins_416(31)
        -- visual/helper ins_269(0)
        -- +60:
        -- unsupported ins_0()
        v_C = (-160)
        v_B = (64)
        -- unsupported ins_435($F, 80, 80, 40, 26)
        i_G = 8
        for _ecl_loop = 1, math.max(0, math.floor(i_G)) do
            -- raw @BossCard5ShadowL() async 0;
            -- visual/helper ins_416(56)
            v_D = ecl_var[-9997]
            v_E = ecl_var[-9996]
            task.MoveTo(v_C, v_B, i_F, 4)
            ecl_sync_self(self)
            task._Wait(i_F)
            ecl_BossCard5_at(self, v_C, v_B, v_D, v_E)
            -- control-flow not structurally lowered: unless ($F > 10) goto BossCard5_1428 @ 60;
            i_F = i_F - 10
            -- label BossCard5_1428
            v_C = v_C * (-1)
            v_B = v_B + (32)
            -- unsupported ins_17(0)
        end
        -- unsupported ins_448(60, 120, 90, 30)
        -- visual/helper ins_263(0, 119)
        -- visual/helper ins_416(31)
        -- visual/helper ins_269(0)
        -- +60:
        -- unsupported ins_0()
        v_C = (128)
        v_B = (64)
        -- unsupported ins_435($F, 80, 80, 40, 26)
        i_H = 8
        for _ecl_loop = 1, math.max(0, math.floor(i_H)) do
            -- raw @BossCard5ShadowL() async 0;
            -- visual/helper ins_416(56)
            v_D = ecl_var[-9997]
            v_E = ecl_var[-9996]
            task.MoveTo(v_C, v_B, i_F, 4)
            ecl_sync_self(self)
            task._Wait(i_F)
            ecl_BossCard5_at(self, v_C, v_B, v_D, v_E)
            -- control-flow not structurally lowered: unless ($F > 10) goto BossCard5_2356 @ 120;
            i_F = i_F - 10
            -- label BossCard5_2356
            -- control-flow not structurally lowered: unless (%B == _f(64)) goto BossCard5_2500 @ 120;
            v_B = (320)
            -- control-flow not structurally lowered: goto BossCard5_2540 @ 120;
            -- label BossCard5_2500
            v_B = (64)
            -- label BossCard5_2540
            v_C = v_C - (42)
            -- unsupported ins_17(0)
        end
        -- unsupported ins_448(60, 120, 90, 30)
        -- +60:
        -- visual/helper ins_263(0, 119)
        -- visual/helper ins_416(31)
        -- visual/helper ins_269(0)
        -- +60:
        -- unsupported ins_0()
        v_C = (160)
        v_B = (288)
        -- unsupported ins_435($F, 80, 80, 40, 26)
        i_I = 8
        for _ecl_loop = 1, math.max(0, math.floor(i_I)) do
            -- raw @BossCard5ShadowL() async 0;
            -- visual/helper ins_416(56)
            v_D = ecl_var[-9997]
            v_E = ecl_var[-9996]
            task.MoveTo(v_C, v_B, i_F, 4)
            ecl_sync_self(self)
            task._Wait(i_F)
            ecl_BossCard5_at(self, v_C, v_B, v_D, v_E)
            -- control-flow not structurally lowered: unless ($F > 10) goto BossCard5_3392 @ 240;
            i_F = i_F - 10
            -- label BossCard5_3392
            v_C = v_C * (-1)
            v_B = v_B - (32)
            -- unsupported ins_17(0)
        end
        -- unsupported ins_448(60, 120, 90, 30)
        -- +60:
        -- visual/helper ins_263(0, 119)
        -- visual/helper ins_416(31)
        -- visual/helper ins_269(0)
        -- +60:
        -- unsupported ins_0()
        v_C = (-128)
        v_B = (320)
        -- unsupported ins_435($F, 80, 80, 40, 26)
        i_J = 8
        for _ecl_loop = 1, math.max(0, math.floor(i_J)) do
            -- raw @BossCard5ShadowL() async 0;
            -- visual/helper ins_416(56)
            v_D = ecl_var[-9997]
            v_E = ecl_var[-9996]
            task.MoveTo(v_C, v_B, i_F, 4)
            ecl_sync_self(self)
            task._Wait(i_F)
            ecl_BossCard5_at(self, v_C, v_B, v_D, v_E)
            -- control-flow not structurally lowered: unless ($F > 10) goto BossCard5_4320 @ 360;
            i_F = i_F - 10
            -- label BossCard5_4320
            -- control-flow not structurally lowered: unless (%B == _f(64)) goto BossCard5_4464 @ 360;
            v_B = (320)
            -- control-flow not structurally lowered: goto BossCard5_4504 @ 360;
            -- label BossCard5_4464
            v_B = (64)
            -- label BossCard5_4504
            v_C = v_C + (42)
            -- unsupported ins_17(0)
        end
        -- unsupported ins_448(60, 120, 90, 30)
    end
    do return end
end
M.BossCard5 = ecl_BossCard5

function ecl_BossCard5_at(self, v_A, v_B, v_C, v_D)
    ecl_sync_self(self)
    local i_A = v_A or 0
    local i_B = v_B or 0
    local i_C = v_C or 0
    local i_D = v_D or 0
    local v_E, i_E, v_F, i_F, v_G, i_G, v_H, i_H, v_I, i_I, v_J, i_J, v_K, i_K, v_L, i_L = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    i_J = 0
    v_E = v_C - v_A
    v_F = v_D - v_B
    v_G = ecl_var[-9965] - v_A
    v_H = ecl_var[-9964] - v_B
    v_I = (v_E * v_H) - (v_F * v_G)
    -- control-flow not structurally lowered: unless (%I < _f(0)) goto BossCard5_at_672 @ 0;
    v_I = 0.20944
    -- control-flow not structurally lowered: goto BossCard5_at_712 @ 0;
    -- label BossCard5_at_672
    v_I = -0.20944
    -- label BossCard5_at_712
    v_E = v_E / (60)
    v_F = v_F / (60)
    -- etNew(0)
    -- etAim et=0 mode=0
    -- etSprite et=0 style=3 color=6
    -- etCount et=0 ways=1 layers=1
    -- etAngle et=0 angle=ecl_rad(0.0) step=ecl_rad(0.62831855)
    -- etSpeed et=0 speed=0.0 step=1.0
    -- etEx et=0 params preserved
    -- etEx et=0 params preserved
    v_K = 1.5707964 + (0 / (16))
    -- etEx et=0 params preserved
    i_L = 61
    for _ecl_loop = 1, math.max(0, math.floor(i_L)) do
        -- etAngle et=0 angle=ecl_rad(v_K) step=ecl_rad(0.0)
        -- etEx et=0 params preserved
        -- etOffsetAbs et=0 x=v_A y=v_B
        liu_10_mc.bullet.ShotBulletMode(0, 0, _editor_class["ecl_stage06_boss_Bullet_3_6"], self.x, self.y, (v_A) - self.x, (v_B) - self.y, 16.0, 0, 0, math.max(1, math.floor(1)), math.max(1, math.floor(1)), 0.0, 1.0, ecl_rad(v_K), ecl_rad(0.0), {{3, 0, 4, 60, -999999, 0.023333333, -999.0}})
        v_A = v_A + v_E
        v_B = v_B + v_F
        v_K = v_K + v_I
    end
    do return end
end
M.BossCard5_at = ecl_BossCard5_at

function ecl_BossCard6(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E, v_F, i_F, v_G, i_G, v_H, i_H, v_I, i_I, v_J, i_J, v_K, i_K, v_L, i_L, v_M, i_M = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    -- timerReset
    -- unsupported ins_21()
    -- boss/meta ins_425()
    -- unsupported ins_256("Ecl_EtBreak", 0.0f, 0.0f, 9999, 0, 0)
    -- boss/meta ins_423()
    -- visual/helper ins_529(0)
    -- visual/helper ins_445()
    -- visual/helper ins_416(28)
    SetV2(self, 0.0, 0.0, true, false)
    task.New(self, function() SetV2(self, 0.0, 0.0, true, false); task._Wait(0) end)
    task.MoveTo(0.0, 0.0, 0, 0)
    ecl_sync_self(self)
    ecl_var[-9949] = 0
    ecl_var[-9948] = 0
    -- boss/meta ins_424(44)
    task.MoveTo(0.0, 128.0, 120, 4)
    ecl_sync_self(self)
    -- setInterrupt phase=0 life=0 time=7200 sub="BossDead"
    -- boss/meta ins_437(96, 7200, 500000, "�򔫁u�t���C���O�t�@���^�X�e�B�J�v")
    -- boss/meta ins_439(98, 7200, 500000, "�򔫁u�`���̔��~�Ձv")
    -- boss/meta ins_422(99, 7200, 500000, "�򔫁u�`���̔��~�Ձv")
    -- unsupported ins_415(70)
    -- unsupported ins_405()
    task._Wait(60)
    -- visual/helper ins_416(58)
    -- visual/helper ins_259(3, 48)
    -- visual/helper ins_259(4, 57)
    -- visual/helper ins_259(5, 49)
    -- visual/helper ins_259(6, 50)
    -- visual/helper ins_259(7, 51)
    -- visual/helper ins_259(8, 52)
    -- visual/helper ins_259(9, 53)
    -- visual/helper ins_259(10, 54)
    -- visual/helper ins_259(11, 55)
    -- visual/helper ins_259(12, 56)
    -- unsupported ins_281(3, 0)
    -- unsupported ins_281(4, 0)
    -- unsupported ins_281(5, 0)
    -- unsupported ins_281(6, 0)
    -- unsupported ins_281(7, 0)
    -- unsupported ins_281(8, 0)
    -- unsupported ins_281(9, 0)
    -- unsupported ins_281(10, 0)
    -- unsupported ins_281(11, 0)
    -- unsupported ins_281(12, 0)
    task.New(self, function() ecl_BossEyes(self) end)
    task._Wait(60)
    -- visual/helper ins_416(28)
    self.x, self.y = 80.0, 80.0
    ecl_sync_self(self)
    v_B = (32)
    i_G = 300
    i_H = 24
    i_I = 0
    i_J = 7200
    i_K = 0
    i_L = 0
    i_M = 1
    -- unsupported ins_446(1, 0.0f)
    ecl_var[-9985] = 6
    ecl_var[-9983] = 1
    while true do
        i_J = i_J - i_G
        -- unsupported ins_436(%F, 0.02617994f, 0.02617994f, 0.028559932f, 0.03141593f)
        -- control-flow not structurally lowered: unless ($K == 0) goto BossCard6_3316 @ 0;
        task.New(self, function() ecl_BossCard6_at(self, 0, (-114) + ecl_var[-9997], (54) + ecl_var[-9996], (0) - v_F, i_H, i_L, i_M) end)
        i_M = i_M + 1
        task.New(self, function() ecl_BossCard6_at(self, 0, (114) + ecl_var[-9997], (54) + ecl_var[-9996], v_F, i_H, i_L, i_M) end)
        i_M = i_M + 1
        task.New(self, function() ecl_BossCard6_at(self, 0, (-64) + ecl_var[-9997], (-80) + ecl_var[-9996], v_F, i_H, i_L, i_M) end)
        i_M = i_M + 1
        task.New(self, function() ecl_BossCard6_at(self, 0, (64) + ecl_var[-9997], (-80) + ecl_var[-9996], (0) - v_F, i_H, i_L, i_M) end)
        i_M = i_M + 1
        i_K = 1
        i_L = 1 - i_L
        -- control-flow not structurally lowered: goto BossCard6_4588 @ 0;
        -- label BossCard6_3316
        task.New(self, function() ecl_BossCard6_at(self, 0, (-114) + ecl_var[-9997], (54) + ecl_var[-9996], v_F, i_H, i_L, i_M) end)
        i_M = i_M + 1
        task.New(self, function() ecl_BossCard6_at(self, 0, (114) + ecl_var[-9997], (54) + ecl_var[-9996], (0) - v_F, i_H, i_L, i_M) end)
        i_M = i_M + 1
        task.New(self, function() ecl_BossCard6_at(self, 0, (-64) + ecl_var[-9997], (-80) + ecl_var[-9996], (0) - v_F, i_H, i_L, i_M) end)
        i_M = i_M + 1
        task.New(self, function() ecl_BossCard6_at(self, 0, (64) + ecl_var[-9997], (-80) + ecl_var[-9996], v_F, i_H, i_L, i_M) end)
        i_M = i_M + 1
        i_K = 0
        -- label BossCard6_4588
        task._Wait(i_G)
        -- control-flow not structurally lowered: unless ($I == 0) goto BossCard6_4968 @ 0;
        -- control-flow not structurally lowered: unless ([-9954] < 5000) goto BossCard6_4944 @ 0;
        i_G = 250
        -- unsupported ins_435($H, 12, 20, 24, 24)
        -- visual/helper ins_416(28)
        i_I = 1
        ecl_var[-9985] = 8
        -- label BossCard6_4944
        -- control-flow not structurally lowered: goto BossCard6_6024 @ 0;
        -- label BossCard6_4968
        -- control-flow not structurally lowered: unless ($I == 1) goto BossCard6_5328 @ 0;
        -- control-flow not structurally lowered: unless ([-9954] < 4000) goto BossCard6_5304 @ 0;
        i_G = 230
        -- unsupported ins_435($H, 14, 22, 26, 26)
        -- visual/helper ins_416(28)
        i_I = 2
        ecl_var[-9985] = 13
        -- label BossCard6_5304
        -- control-flow not structurally lowered: goto BossCard6_6024 @ 0;
        -- label BossCard6_5328
        -- control-flow not structurally lowered: unless ($I == 2) goto BossCard6_5688 @ 0;
        -- control-flow not structurally lowered: unless ([-9954] < 3000) goto BossCard6_5664 @ 0;
        i_G = 200
        -- unsupported ins_435($H, 14, 26, 26, 28)
        -- visual/helper ins_416(28)
        ecl_var[-9985] = 4
        i_I = 3
        -- label BossCard6_5664
        -- control-flow not structurally lowered: goto BossCard6_6024 @ 0;
        -- label BossCard6_5688
        -- control-flow not structurally lowered: unless ($I == 3) goto BossCard6_6024 @ 0;
        -- control-flow not structurally lowered: unless ([-9954] < 2000) goto BossCard6_6024 @ 0;
        i_G = 150
        -- unsupported ins_435($H, 14, 26, 26, 30)
        -- visual/helper ins_416(28)
        ecl_var[-9985] = 2
        i_I = 4
        -- label BossCard6_6024
        -- control-flow not structurally lowered: unless ($I != 5) goto BossCard6_6512 @ 0;
        -- control-flow not structurally lowered: unless ($J < (36 * 60)) goto BossCard6_6512 @ 0;
        i_G = i_G - 10
        i_I = 5
        i_G = 150
        -- unsupported ins_435($H, 18, 32, 32, 32)
        -- visual/helper ins_416(28)
        ecl_var[-9985] = 2
        i_I = 5
    end
    do return end
end
M.BossCard6 = ecl_BossCard6

function ecl_BossCard6_at(self, v_A, v_B, v_C, v_D, v_E, v_F, v_G)
    ecl_sync_self(self)
    local i_A = v_A or 0
    local i_B = v_B or 0
    local i_C = v_C or 0
    local i_D = v_D or 0
    local i_E = v_E or 0
    local i_F = v_F or 0
    local i_G = v_G or 0
    local v_H, i_H, v_I, i_I = 0, 0, 0, 0
    -- etNew(i_A)
    -- etAim et=i_A mode=3
    -- etSprite et=i_A style=10 color=ecl_var[-9985]
    -- etCount et=i_A ways=i_E layers=1
    -- etAngle et=i_A angle=ecl_rad(0) step=ecl_rad(0.62831855)
    -- etSpeedD et=i_A speed=ecl_pick_rank(1.5, 1.5, 1.7, 1.8) step=ecl_pick_rank(1.0, 1.0, 1.0, 1.0)
    -- etEx et=i_A params preserved
    -- etEx et=i_A params preserved
    -- etEx et=i_A params preserved
    -- etEx et=i_A params preserved
    -- etEx et=i_A params preserved
    -- etEx et=i_A params preserved
    -- control-flow not structurally lowered: unless ($F != 0) goto BossCard6_at_636 @ 0;
    -- unsupported ins_520(%H, %B, %C)
    -- control-flow not structurally lowered: goto BossCard6_at_676 @ 0;
    -- label BossCard6_at_636
    v_H = 1.570796
    -- label BossCard6_at_676
    -- unsupported ins_436(%I, 0.5f, 0.5f, 0.55f, 0.6f)
    ecl_var[-9981] = v_H
    ecl_var[-9980] = v_I
    -- etEx et=i_A params preserved
    -- etEx et=i_A params preserved
    -- etOffsetAbs et=i_A x=v_B y=v_C
    liu_10_mc.bullet.ShotBulletMode(3, i_A, _editor_class["ecl_stage06_boss_Bullet_10_ecl_var_9985"], self.x, self.y, (v_B) - self.x, (v_C) - self.y, 0, 0, 0, math.max(1, math.floor(i_E)), math.max(1, math.floor(1)), ecl_pick_rank(1.5, 1.5, 1.7, 1.8), ecl_pick_rank(1.0, 1.0, 1.0, 1.0), ecl_rad(0), ecl_rad(0.62831855), {{7, 1, 8, 60000, -999999, 0.0, v_D / 4.8}})
    ecl_var[-9983] = i_G
    -- unsupported ins_257("BossCard6_atLine", %B, %C, 100, 100, 0)
    do return end
end
M.BossCard6_at = ecl_BossCard6_at

function ecl_BossCard6_atLine(self)
    ecl_sync_self(self)
    local v_A, i_A = 0, 0
    -- visual/helper ins_258(2)
    -- visual/helper ins_259(0, 82)
    -- unsupported ins_402(271)
    task._Wait(14)
    SetV2(self, ecl_var[-9980], ecl_var[-9981], true, false)
    -- visual/helper ins_529(6)
    while true do
        task._Wait(1000)
    end
    do return end
end
M.BossCard6_atLine = ecl_BossCard6_atLine

function ecl_BossCard6_atLineDead(self)
    ecl_sync_self(self)
    -- unsupported ins_402(32)
    do return end
    do return end
end
M.BossCard6_atLineDead = ecl_BossCard6_atLineDead

function ecl_BossEyes(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C = 0, 0, 0, 0, 0, 0
    while true do
        v_B = ecl_var[-9997] + (-114)
        v_C = ecl_var[-9996] + (54)
        -- unsupported ins_520(%A, %B, %C)
        v_B = math.cos(v_A) * (6.0)
        v_C = math.sin(v_A) * (6.0)
        -- unsupported ins_279(9, %B, %C)
        v_B = ecl_var[-9997] + (114)
        v_C = ecl_var[-9996] + (54)
        -- unsupported ins_520(%A, %B, %C)
        v_B = math.cos(v_A) * (6.0)
        v_C = math.sin(v_A) * (6.0)
        -- unsupported ins_279(10, %B, %C)
        v_B = ecl_var[-9997] + (-64)
        v_C = ecl_var[-9996] + (-80)
        -- unsupported ins_520(%A, %B, %C)
        v_B = math.cos(v_A) * (6.0)
        v_C = math.sin(v_A) * (6.0)
        -- unsupported ins_279(11, %B, %C)
        v_B = ecl_var[-9997] + (64)
        v_C = ecl_var[-9996] + (-80)
        -- unsupported ins_520(%A, %B, %C)
        v_B = math.cos(v_A) * (6.0)
        v_C = math.sin(v_A) * (6.0)
        -- unsupported ins_279(12, %B, %C)
        task._Wait(1)
    end
    do return end
end
M.BossEyes = ecl_BossEyes

function ecl_BossEyes2(self)
    ecl_sync_self(self)
    local v_A, i_A, v_B, i_B, v_C, i_C, v_D, i_D, v_E, i_E, v_F, i_F, v_G, i_G, v_H, i_H = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    v_A = 1.570796
    v_B = 1.570796
    v_C = 1.570796
    v_D = 1.570796
    v_E = math.cos(v_A) * (6.0)
    v_F = math.sin(v_A) * (6.0)
    -- unsupported ins_279(9, %E, %F)
    -- unsupported ins_279(10, %E, %F)
    -- unsupported ins_279(11, %E, %F)
    -- unsupported ins_279(12, %E, %F)
    task._Wait(100)
    i_G = 0
    -- unsupported ins_435($H, 10, 10, 9, 7)
    while true do
        v_E = math.cos(v_A) * (6.0)
        v_F = math.sin(v_A) * (6.0)
        -- unsupported ins_279(9, %E, %F)
        -- control-flow not structurally lowered: unless (($G % $H) == 0) goto BossEyes2_808 @ 0;
        ecl_BossCard2_at1(self, v_A, (-114) + ecl_var[-9997], (54) + ecl_var[-9996])
        -- label BossEyes2_808
        v_A = v_A + 0.031416
        -- unsupported ins_82(%A)
        v_E = math.cos(v_B) * (6.0)
        v_F = math.sin(v_B) * (6.0)
        -- unsupported ins_279(10, %E, %F)
        -- control-flow not structurally lowered: unless (($G % $H) == 0) goto BossEyes2_1252 @ 0;
        ecl_BossCard2_at1(self, v_B, (114) + ecl_var[-9997], (54) + ecl_var[-9996])
        -- label BossEyes2_1252
        v_B = v_B - 0.031416
        -- unsupported ins_82(%B)
        v_E = math.cos(v_C) * (6.0)
        v_F = math.sin(v_C) * (6.0)
        -- unsupported ins_279(11, %E, %F)
        -- control-flow not structurally lowered: unless (($G % $H) == 0) goto BossEyes2_1696 @ 0;
        ecl_BossCard2_at1(self, v_C, (-64) + ecl_var[-9997], (-80) + ecl_var[-9996])
        -- label BossEyes2_1696
        v_C = v_C + 0.020944
        -- unsupported ins_82(%C)
        v_E = math.cos(v_D) * (6.0)
        v_F = math.sin(v_D) * (6.0)
        -- unsupported ins_279(12, %E, %F)
        -- control-flow not structurally lowered: unless (($G % $H) == 0) goto BossEyes2_2140 @ 0;
        ecl_BossCard2_at1(self, v_D, (64) + ecl_var[-9997], (-80) + ecl_var[-9996])
        -- label BossEyes2_2140
        v_D = v_D - 0.020944
        -- unsupported ins_82(%D)
        task._Wait(1)
        i_G = i_G + 1
    end
    do return end
end
M.BossEyes2 = ecl_BossEyes2

function ecl_HPWait(self, v_A, v_B)
    ecl_sync_self(self)
    local i_A = v_A or 0
    local i_B = v_B or 0
    for _ecl_loop = 1, math.max(0, math.floor(i_B)) do
        -- control-flow not structurally lowered: unless ([-9954] <= $A) goto HPWait_164 @ 0;
        -- control-flow not structurally lowered: goto HPWait_228 @ 0;
        -- label HPWait_164
        task._Wait(1)
    end
    -- label HPWait_228
    do return end
end
M.HPWait = ecl_HPWait

-- Bullet classes synthesized from ECL etSprite state
_editor_class["ecl_stage06_boss_Bullet_0_6"] = _editor_class["ecl_stage06_boss_Bullet_0_6"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_0_6"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 0, 6)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_10_ecl_var_9985"] = _editor_class["ecl_stage06_boss_Bullet_10_ecl_var_9985"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_10_ecl_var_9985"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 10, ecl_var[-9985])
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_11_6"] = _editor_class["ecl_stage06_boss_Bullet_11_6"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_11_6"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 11, 6)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_15_6"] = _editor_class["ecl_stage06_boss_Bullet_15_6"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_15_6"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 15, 6)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_17_1"] = _editor_class["ecl_stage06_boss_Bullet_17_1"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_17_1"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 17, 1)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_17_2"] = _editor_class["ecl_stage06_boss_Bullet_17_2"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_17_2"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 17, 2)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_17_3"] = _editor_class["ecl_stage06_boss_Bullet_17_3"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_17_3"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 17, 3)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_1_0"] = _editor_class["ecl_stage06_boss_Bullet_1_0"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_1_0"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 1, 0)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_21_3"] = _editor_class["ecl_stage06_boss_Bullet_21_3"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_21_3"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 21, 3)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_26_0"] = _editor_class["ecl_stage06_boss_Bullet_26_0"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_26_0"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 26, 0)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_26_1"] = _editor_class["ecl_stage06_boss_Bullet_26_1"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_26_1"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 26, 1)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_28_4"] = _editor_class["ecl_stage06_boss_Bullet_28_4"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_28_4"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 28, 4)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_29_0"] = _editor_class["ecl_stage06_boss_Bullet_29_0"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_29_0"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 29, 0)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_3_1"] = _editor_class["ecl_stage06_boss_Bullet_3_1"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_3_1"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 3, 1)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_3_6"] = _editor_class["ecl_stage06_boss_Bullet_3_6"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_3_6"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 3, 6)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_7_13"] = _editor_class["ecl_stage06_boss_Bullet_7_13"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_7_13"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 7, 13)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_7_2"] = _editor_class["ecl_stage06_boss_Bullet_7_2"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_7_2"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 7, 2)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

_editor_class["ecl_stage06_boss_Bullet_7_4"] = _editor_class["ecl_stage06_boss_Bullet_7_4"] or Class(bullet)
do
    local bullet_class = _editor_class["ecl_stage06_boss_Bullet_7_4"]
    function bullet_class:init(x, y, ...)
        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)
        self.x, self.y = x, y
        liu_10_mc.bullet.BulletClassInit(self, 7, 4)
        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)
    end
end

function M.attach_to_boss_card(card)
    task.New(card, function()
        ecl_Boss(card)
    end)
end

return M