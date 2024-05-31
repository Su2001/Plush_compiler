function main(val args:[string]) {
    val actual : [int] := newarray[6];
	actual[0] :=1;
	actual[1] :=6;
	actual[2] :=7;
	actual[3] :=4;
	actual[4] :=21;
	actual[5] :=67;
	var target: int := 4;
	var count : int := 0;
	var result : int := -1;
	while count < 6 && result == -1 {
		if actual[count] == target{
			result := count;
		}
		count := count + 1;
	}
	print_int(result);
}
