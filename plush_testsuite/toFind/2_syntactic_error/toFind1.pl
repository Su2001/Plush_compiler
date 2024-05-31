val actual : [int] := [1,2,3,4,5,6,7,9,1,1,2];

function toFind(val targetArray:[int], val length: int, val target:int) : int {# Find the first enconter element and return the position if not encontered return -1
	var count : int := 0;
	var result : int := -1;
	while count < length && result != -1 {
		if targetArray[count] == target{
			result := count;
		
		count := count + 1;
	} 
	toFind := result; # This line returns the first enconter element
}


function main(val args:[string]) {
	val result : int := toFind(targetArray, 11, 4);
	print_int(result);
}
