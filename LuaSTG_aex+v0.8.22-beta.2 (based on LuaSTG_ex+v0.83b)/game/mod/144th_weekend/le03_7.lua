le03_7_background = Class(object)

function le03_7_background:init()
    background.init(self,false)
	LoadImageFromFile('ground','ground.jpg')
    SetImageState('ground','mul+alpha',Color(255,118,106,94))
    LoadImageFromFile('road','road.png')
    LoadImageFromFile('tree1','tree1.png')
    LoadImageFromFile('tree2','tree2.png')
    LoadImageFromFile('clouds','clouds.png')
    SetImageState('clouds','mul+alpha',Color(220,255,255,255))
    LoadImageFromFile('wu','wu.png')
    LoadImageFromFile('wu_rev','wu_rev.png')
    SetImageState('wu','mul+alpha',Color(122,255,255,255))
    SetImageState('wu_rev','mul+alpha',Color(122,255,255,255))
    LoadImageFromFile('sky','LHX_sky.png')
    SetImageState('sky','mul+alpha',Color(255,100,100,255))
    LoadImageFromFile('snow','LHX_snow.png')
	Set3D('eye',0,1.9,0)
	Set3D('at',0,1.4,2)
	Set3D('up',0,1,0)
	Set3D('fovy',0.6)
	Set3D('z',0.01,20)
	Set3D('fog',7,20,Color(200,199,199,199))
	self.zos=0
	self.speed=0.02
end

function le03_7_background:frame()
	self.zos = self.zos + self.speed
    if IsValid(_boss) and _boss.cards[_boss.card_num] and _boss.cards[_boss.card_num].is_sc then
	else
		if self.timer%10==0 then
			for i=1,ran:Int(2,5) do
				local size=ran:Float(0.2,2)
				local x=ran:Float(-224,224)
				local y=ran:Float(300,320)
				local alpha = ran:Int(100,155)
				New(le03_7_snow,'snow',x,y,ran:Float(1,3),270+ran:Int(-10,10),size,alpha)
			end
		end
	end
end

function le03_7_background:render()
	SetViewMode'3d'
	background.WarpEffectCapture()
	background.ClearToFogColor()
	local z=self.zos%1
	local d=0.5
    RenderWu(self.timer)
    RenderGrounds(-z)
    RenderClouds(-z*6)
    RenderTrees(-z)
    Render4V('sky',-2,0,1, 2,0,1, 2,2.9,1, -2,2.9,1)
	
	background.WarpEffectApply()
	SetViewMode'world'
end

function RenderClouds(z)
    local dx = 0.2
    local height = 1.93
    for i= 0,20 do
        for j = -2,4,2 do
            Render4V('clouds',-1.5+dx+j,height,z+i, -0.5+dx+j,height,z+i, -0.5+dx+j,height,z+1+i, -1.5+dx+j,height,z+1+i)
            Render4V('clouds',-0.5+dx+j,height,z+i+0.5, 0.5+dx+j,height,z+i+0.5, 0.5+dx+j,height,z+1.5+i, -0.5+dx+j,height,z+1.5+i)
        end
        dx = - dx
    end
end
function RenderGrounds(z)
    for i =20,-2,-1 do
        Render4V('ground',-1.1,0.9,z+i+1  , -0.6,0.7,z+i+0.7, -0.3,0,z+i+1    , -0.305,0.002,z+i+1.003) --左侧前
        Render4V('ground',1.1,0.9,z+i+1   , 0.6,0.7,z+i+0.7 , 0.3,0,z+i+1     , 0.305,0.002,z+i+1.003) --右侧前
        Render4V('ground',-0.6,0.7,z+i+0.7, -0.6,0.7,z+i+0.3, -0.3,0,z+i      , -0.3,0,z+1+i) --左侧底
        Render4V('ground',0.6,0.7,z+i+0.7 , 0.6,0.7,z+i+0.3 , 0.3,0,z+i       , 0.3,0,z+1+i) --右侧底
        Render4V('ground',-1.1,0.9,z+i    , -0.6,0.7,z+i+0.3, -0.3,0,z+i      , -0.305,0.002,z+i-0.003) --左侧后
        Render4V('ground',1.1,0.9,z+i     , 0.6,0.7,z+i+0.3 , 0.3,0,z+i       , 0.305,0.002,z+i-0.003) --右侧后
        Render4V('ground',-1.1,0.9,z+i    , -1.1,0.9,z+1+i  , -0.6,0.7,z+i+0.7, -0.6,0.7,z+i+0.3) --左侧顶
        Render4V('ground',1.1,0.9,z+i     , 1.1,0.9,z+1+i   , 0.6,0.7,z+i+0.7 , 0.6,0.7,z+i+0.3) --右侧顶
        Render4V('ground',-0.3,0,z+i      , 0,-0.1,z+i       , 0,-0.1,z+1+i     , -0.3,0,z+1+i) --底面
        Render4V('ground',0.3,0,z+i       , 0,-0.1,z+i       , 0,-0.1,z+1+i     , 0.3,0,z+1+i) --底面
        Render4V('ground',-1.3,1,z+i      , -1.1,0.9,z+i    , -1.1,0.9,z+1+i  , -1.3,1,z+1+i) --左边
        Render4V('ground',1.1,0.9,z+i     , 1.3,1,z+i       , 1.3,1,z+1+i     , 1.1,0.9,z+1+i) --右边
        Render4V('road'  ,-1.3,1,z+i      , -3,1,z+i        , -3,1,z+1+i      , -1.3,1,z+1+i)  --左边路
        Render4V('road'  ,1.3,1,z+i       , 3,1,z+i         , 3,1,z+1+i       , 1.3,1,z+1+i)  --右边路
    end
end
function RenderTrees(z)
    for i =1,30 do
        Render4V('tree1',-2.5,1.6,z+i ,-2,1.6,z+i  ,-2,1,z+i ,-2.5,1,z+i)
        Render4V('tree2',2,1.6,z+i    , 2.5,1.6,z+i,2.5,1,z+i,2,1,z+i   )
    end
end
function RenderWu(t)
    Render4V('clouds',-1.5,1.5,16.5, 1.5,1.5,16.5, 1.5,2.5,16.5, -1.5,2.5,16.5)
    if t % 3600 < 1800 then
        Render4V('wu_rev',sin(t/10)/2,2,16,-sin(t/10)/2,2,16,-sin(t/10)/2,1,16,sin(t/10)/2,1,16)
    else
        Render4V('wu',sin((t-1800)/10)/2,2,16,-sin((t-1800)/10)/2,2,16,-sin((t-1800)/10)/2,1,16,sin((t-1800)/10)/2,1,16)
    end
end

le03_7_snow = Class(object)
function le03_7_snow:init(img,x,y,v,rot,size,a)
    self.img = img
    self.x = x
    self.y = y
    self.angle = rot
    self.v = v
    self.hscale = size  self.vscale = size
    self.size = size
    self.color = color
    self.group=GROUP_GHOST
    self.bound = false
    self.layer=LAYER_BG+5
    self.a = a
    self.omiga=ran:Float(-3,-2) 
end

function le03_7_snow:frame()
    self.x = self.x + self.v*cos(self.angle)
    self.y = self.y + self.v*sin(self.angle)
    self.hscale = self.size * cos(self.timer - 30)
    self.vscale = self.size * sin(self.timer + 30)
    self.color = Color(self.a,255,255,255)
    self.size = self.size - 0.002
    self.a = self.a - 0.5
    if IsValid(_boss) and _boss.cards[_boss.card_num] and _boss.cards[_boss.card_num].is_sc then
        Del(self)
    end
    if self.a < 1 then 
        Del(self)
    end
end 

function le03_7_snow:render()
	SetImageState(self.img,"mul+add",self.color)
	SetViewMode"world"
	object.render(self)
	SetImageState(self.img,"",Color(255,255,255,255))
end