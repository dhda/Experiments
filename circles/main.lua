function table.copy(t)
	local u = { }
	for k, v in pairs(t) do u[k] = v end
	return setmetatable(u, getmetatable(t))
end

function drawCircle(c)
	love.graphics.circle("line", c.x, c.y, c.r, 100)
end


circles = {}
cont    = {x=love.graphics.getWidth()/2, y=love.graphics.getHeight()/2, r=math.min(love.graphics.getWidth(), love.graphics.getHeight())/2}

carea   = math.pi * math.pow(cont.r,2)
area    = carea / 4.0
rad     = math.sqrt(area / math.pi)
curmax  = 2*math.ceil(carea/area)

iters = 0
tries = curmax

function love.load()
	circles = {}
	
	carea   = math.pi * math.pow(cont.r,2)
	area    = carea / 4.0
	rad     = math.sqrt(area / math.pi)
	curmax  = 2*math.ceil(carea/area)
	
	iters   = 0
	tries   = curmax
end


function love.update(dt)
	if iters < 50 then
		if tries == curmax then
			iters = iters+1
			tries = 0

			area   = area * math.pow(iters, -0.1)
			rad    = math.sqrt(area / math.pi)
			curmax = 2*math.ceil(carea/area)
		else
			while tries ~= curmax do
				r     = math.random() * (cont.r-rad)
				theta = math.random() * (2.0*math.pi)

				x = r*math.cos(theta) + cont.x
				y = r*math.sin(theta) + cont.y


				good = true

				for i,c in ipairs(circles) do
					d = math.sqrt(math.pow(x-c.x,2.0) + math.pow(y-c.y,2.0))
					if d < c.r+rad then
						x = x + (c.r + rad - d)*math.cos(math.acos((x-c.x)/d))
						y = y + (c.r + rad - d)*math.sin(math.asin((y-c.y)/d))
					end
				end

				d = math.sqrt((x-cont.x)^2 + (y-cont.y)^2)
				if d >= cont.r-rad then
					x = x + ((cont.r-rad) - d)*math.cos(math.acos((x-cont.x)/d))
					y = y + ((cont.r-rad) - d)*math.sin(math.asin((y-cont.y)/d))
				end

				for i,c in ipairs(circles) do
					d = math.sqrt(math.pow(x-c.x,2.0) + math.pow(y-c.y,2.0))
					if d < c.r+rad then
						good = false
						break
					end
				end

				if good then
					table.insert(circles, {x=x, y=y, r=rad})
					carea = carea - area/2.0
					tries = tries+1
					break
				end

				tries = tries+1
			end
		end
	end
end


function love.draw()
	love.graphics.setColor(200, 40, 40, 200)
	-- drawCircle(cont)
	
	love.graphics.setColor(40, 40, 200, 255)
	for i,c in ipairs(circles) do
		drawCircle(c)
	end
end


function love.mousepressed(x, y, button)
	love.load()
end
