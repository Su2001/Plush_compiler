val toFind : int := 9;

function isPrime(val target:int) : int {# If target is prime returns 1 else -1
	val max : int := target - 1;
    var count : int := 2;
    val result : int := -1;
	while count <= max && target %. count != 0{
		count := count +1;
	} 
    if target == 1 || count == target {
        result := 1;
    }
	isPrime := result; # This line returns if its prime number
}


function main(val args:[string]) {
	val result : int := isPrime(toFind);
	print_int(result);
}