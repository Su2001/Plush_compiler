val t1 : int := 48;
val t2 : int := 18;

function maxDivisor(val a:int, val b:int) : int # find the largest common divisor
	var temp_a : int := a;
	var temp_b : int := b;
	var temp : int := 0;
	while temp_b != 0{
		temp := temp_b;
		temp_b := temp_a % temp_b;
		temp_a := temp;
	} 
	if a == 0 || b == 0{
		temp_a := 0;
	}
	maxDivisor := temp_a; # This line returns the gcd
}


function main(val args:[string]) {
	val result : int := maxDivisor(t1,t2);
	print_int(result);
}