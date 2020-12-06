function soma(x::Int, y::Int)::Int
local a::Int
a = x + y
println(a)
return a
end
local a::Int
local b::Int
a = 3
b = soma(3, 4)
println(a)
println(b)   