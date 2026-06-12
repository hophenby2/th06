local tex_name = "liu_10_mc_distortion_texture"
CreateRenderTarget(tex_name)


local cut = 16
local min_radius = 16
local const_expand = 20
local const_expand_r = 16
local phasex = 180
local phasey = 90
local phasex_i = 90
local phasey_i = 45
local blow_rangeX = 10
local blow_rangeY = -10
local phase_speedX = 10
local phase_speedY = 5

local canvas_w,canvas_h=640,480

local _w=lstg.world.r-lstg.world.l
local _h=lstg.world.t-lstg.world.b
local _w1,_h1=_w*screen.scale,_h*screen.scale

local _ObjPush = Class(object)
local _ObjPop = Class(object)

function _ObjPush:init(layer_A)
    self.layer = layer_A
    self.group = GROUP_GHOST
end
function _ObjPush:render()
    PushRenderTarget(tex_name)
    RenderClear(Color(0,0,0,0))
end

local function _DrawTexture()
    local _iro = Color(255,255,255,255)
    local bx,by = lstg.world.scrl*screen.scale+screen.dx,(canvas_h-lstg.world.scrt)*screen.scale+screen.dy
    RenderTexture(tex_name,"one",
    {lstg.world.l,lstg.world.t,0.5,bx+0,by+0,_iro},
    {lstg.world.l+_w,lstg.world.t,0.5,bx+_w1,by+0,_iro},
    {lstg.world.l+_w,lstg.world.t-_h,0.5,bx+_w1,by+_h1,_iro},
    {lstg.world.l,lstg.world.t-_h,0.5,bx+0,by+_h1,_iro}
    )
end

function _ObjPop:init(layer_A,layer_B)
    self.layer = layer_B
    self.group = GROUP_GHOST
    self.servant = New(_ObjPush,layer_A)
end
function _ObjPop:render()
    PopRenderTarget()
    _DrawTexture()
end

function liu_10_mc_Distortion_CaptureAndDraw(a,b)
    New(_ObjPop,a,b)
end

local distortion_mesh = {}
local _unit

local function WorldToUv(x,y)
    local bx,by = lstg.world.scrl*screen.scale+screen.dx,(canvas_h-lstg.world.scrt)*screen.scale+screen.dy
    return x*screen.scale+(bx+_w1*0.5),-y*screen.scale+(by+_h1*0.5)
end

for j=1,cut do
    for i=1,cut do
        distortion_mesh[(j-1)*cut+i] = {
            x1=-min_radius+((min_radius*2)/cut)*(i-1),  y1=min_radius-((min_radius*2)/cut)*(j-1),   z1=0.5,
            x2=-min_radius+((min_radius*2)/cut)*(i),   y2=min_radius-((min_radius*2)/cut)*(j-1),   z2=0.5,
            x3=-min_radius+((min_radius*2)/cut)*(i),   y3=min_radius-((min_radius*2)/cut)*(j),  z3=0.5,
            x4=-min_radius+((min_radius*2)/cut)*(i-1),   y4=min_radius-((min_radius*2)/cut)*(j),  z4=0.5,
        }

        _unit = distortion_mesh[(j-1)*cut+i]
        
        _unit.distance1 = Dist(0,0,_unit.x1,_unit.y1)
        _unit.distance2 = Dist(0,0,_unit.x2,_unit.y2)
        _unit.distance3 = Dist(0,0,_unit.x3,_unit.y3)
        _unit.distance4 = Dist(0,0,_unit.x4,_unit.y4)

        _unit.angle1 = Angle(0,0,_unit.x1,_unit.y1)
        _unit.angle2 = Angle(0,0,_unit.x2,_unit.y2)
        _unit.angle3 = Angle(0,0,_unit.x3,_unit.y3)
        _unit.angle4 = Angle(0,0,_unit.x4,_unit.y4)

        _unit.disx1,_unit.disy1 =  _unit.distance1*cos(_unit.angle1),_unit.distance1*sin(_unit.angle1)
        _unit.disx2,_unit.disy2 =  _unit.distance2*cos(_unit.angle2),_unit.distance2*sin(_unit.angle2)
        _unit.disx3,_unit.disy3 =  _unit.distance3*cos(_unit.angle3),_unit.distance3*sin(_unit.angle3)
        _unit.disx4,_unit.disy4 =  _unit.distance4*cos(_unit.angle4),_unit.distance4*sin(_unit.angle4)

        _unit.ratio1 = 1-min(1,max(_unit.distance1/min_radius,0))
        _unit.ratio2 = 1-min(1,max(_unit.distance2/min_radius,0))
        _unit.ratio3 = 1-min(1,max(_unit.distance3/min_radius,0))
        _unit.ratio4 = 1-min(1,max(_unit.distance4/min_radius,0))

        _unit.e_ratio1 = _unit.distance1 >0 and 1-min(1,max(_unit.distance1/const_expand_r,0))^2 or 0
        _unit.e_ratio2 = _unit.distance2 >0 and 1-min(1,max(_unit.distance2/const_expand_r,0))^2 or 0
        _unit.e_ratio3 = _unit.distance3 >0 and 1-min(1,max(_unit.distance3/const_expand_r,0))^2 or 0
        _unit.e_ratio4 = _unit.distance4 >0 and 1-min(1,max(_unit.distance4/const_expand_r,0))^2 or 0

        _unit.phasex1 = phasex + phasex_i*((j-1)*16+i-1)
        _unit.phasex2 = phasex + phasex_i*(j*16+i)
        _unit.phasey1 = phasey + phasey_i*((j-1)*16+i-1)
        _unit.phasey2 = phasey + phasey_i*(j*16+i)

        _unit.u1,_unit.v1 = _unit.x1*screen.scale,-_unit.y1*screen.scale
        _unit.u2,_unit.v2 = _unit.x2*screen.scale,-_unit.y2*screen.scale
        _unit.u3,_unit.v3 = _unit.x3*screen.scale,-_unit.y3*screen.scale
        _unit.u4,_unit.v4 = _unit.x4*screen.scale,-_unit.y4*screen.scale

        _unit.aratio1 = _unit.distance1 >=min_radius and 0 or 1
        _unit.aratio2 = _unit.distance2 >=min_radius and 0 or 1
        _unit.aratio3 = _unit.distance3 >=min_radius and 0 or 1
        _unit.aratio4 = _unit.distance4 >=min_radius and 0 or 1

        _unit.cratio1 = 1-min(1,max(_unit.distance1/min_radius,0))^2
        _unit.cratio2 = 1-min(1,max(_unit.distance2/min_radius,0))^2
        _unit.cratio3 = 1-min(1,max(_unit.distance3/min_radius,0))^2
        _unit.cratio4 = 1-min(1,max(_unit.distance4/min_radius,0))^2
    end
end

liu_10_mc_ObjDistortion = Class(object)

function liu_10_mc_ObjDistortion:init(target,_radius,layer,A,R,G,B)
    self.layer = layer or LAYER_BG+1
    self.color = {A,R,G,B} or {255,255,0,0}
    self.group = GROUP_GHOST
    self.target = target
    self.radius = 20
    self.radius_speed = 2
    self._radius = _radius
    self.count = 0
    self.bound= false

    self.size_factor = 1

    self.x,self.y = target.x or 0,target.y or 0
    self.uvx,self.uvy = WorldToUv(0,0)

    self.mesh=distortion_mesh
    self.mesh_unit = self.mesh[1]
end

function liu_10_mc_ObjDistortion:frame()
    self.radius = min(self.radius+self.radius_speed,self._radius)
    self.size_factor = self.radius/min_radius

    if IsValid(self.target) then
        self.x,self.y = self.target.x,self.target.y
        self.uvx,self.uvy = WorldToUv(self.x,self.y)
        self.count=self.count+1
    else
    		Del(self)
    end
end

local m1,m2,m3,m4
local muni
local k=0.5

function liu_10_mc_ObjDistortion:render()
    for j=1,cut do
        for i=1,cut do
            self.mesh_unit = self.mesh[(j-1)*cut+i]
            muni = self.mesh_unit
            
            m1 = blow_rangeX*cos(self.mesh_unit.phasex1+phase_speedX*self.count)
            m2 = blow_rangeX*cos(self.mesh_unit.phasex2+phase_speedX*self.count)
            m3 = blow_rangeY*sin(self.mesh_unit.phasey1+phase_speedY*self.count)
            m4 = blow_rangeY*sin(self.mesh_unit.phasey2+phase_speedY*self.count)

            RenderTexture(tex_name,"mul+alpha",
            {muni.x1*self.size_factor+self.x+m1*muni.ratio1+muni.disx1*self.size_factor*muni.ratio1*muni.ratio1*k + const_expand*muni.e_ratio1*cos(muni.angle1),
            muni.y1*self.size_factor+self.y+m3*muni.ratio1+muni.disy1*self.size_factor*muni.ratio1*muni.ratio1*k + const_expand*muni.e_ratio1*sin(muni.angle1),
            muni.z1,muni.u1*self.size_factor+self.uvx,muni.v1*self.size_factor+self.uvy,Color(self.color[1]*muni.aratio1,255+(self.color[2]-255)*muni.cratio1,255+(self.color[3]-255)*muni.cratio1,255+(self.color[4]-255)*muni.cratio1)},

            {muni.x2*self.size_factor+self.x+m2*muni.ratio2+muni.disx2*self.size_factor*muni.ratio2*muni.ratio2*k + const_expand*muni.e_ratio2*cos(muni.angle2),
            muni.y2*self.size_factor+self.y+m4*muni.ratio2+muni.disy2*self.size_factor*muni.ratio2*muni.ratio2*k + const_expand*muni.e_ratio2*sin(muni.angle2),
            muni.z2,muni.u2*self.size_factor+self.uvx,muni.v2*self.size_factor+self.uvy,Color(self.color[1]*muni.aratio2,255+(self.color[2]-255)*muni.cratio2,255+(self.color[3]-255)*muni.cratio2,255+(self.color[4]-255)*muni.cratio2)},

            {muni.x3*self.size_factor+self.x+m2*muni.ratio3+muni.disx3*self.size_factor*muni.ratio3*muni.ratio3*k + const_expand*muni.e_ratio3*cos(muni.angle3),
            muni.y3*self.size_factor+self.y+m4*muni.ratio3+muni.disy3*self.size_factor*muni.ratio3*muni.ratio3*k + const_expand*muni.e_ratio3*sin(muni.angle3),
            muni.z3,muni.u3*self.size_factor+self.uvx,muni.v3*self.size_factor+self.uvy,Color(self.color[1]*muni.aratio3,255+(self.color[2]-255)*muni.cratio3,255+(self.color[3]-255)*muni.cratio3,255+(self.color[4]-255)*muni.cratio3)},

            {muni.x4*self.size_factor+self.x+m1*muni.ratio4+muni.disx4*self.size_factor*muni.ratio4*muni.ratio4*k + const_expand*muni.e_ratio4*cos(muni.angle4),
            muni.y4*self.size_factor+self.y+m3*muni.ratio4+muni.disy4*self.size_factor*muni.ratio4*muni.ratio4*k + const_expand*muni.e_ratio4*sin(muni.angle4),
            muni.z4,muni.u4*self.size_factor+self.uvx,muni.v4*self.size_factor+self.uvy,Color(self.color[1]*muni.aratio4,255+(self.color[2]-255)*muni.cratio4,255+(self.color[3]-255)*muni.cratio4,255+(self.color[4]-255)*muni.cratio4)}
            )
        end
    end
end

function liu_10_mc_Distortion_Apply(target,_radius,layer,A,R,G,B)
    target.distortion = New(liu_10_mc_ObjDistortion,target,_radius,layer,A,R,G,B)
end
