
define void @"main"(i8** %"args")
{
main_entry:
  %".3" = alloca i8**
  store i8** %"args", i8*** %".3"
  %".5" = alloca [6 x i32]
  %".6" = getelementptr [6 x i32], [6 x i32]* %".5", i32 0, i32 0
  store i32 1, i32* %".6"
  %".8" = getelementptr [6 x i32], [6 x i32]* %".5", i32 0, i32 1
  store i32 6, i32* %".8"
  %".10" = getelementptr [6 x i32], [6 x i32]* %".5", i32 0, i32 2
  store i32 7, i32* %".10"
  %".12" = getelementptr [6 x i32], [6 x i32]* %".5", i32 0, i32 3
  store i32 4, i32* %".12"
  %".14" = getelementptr [6 x i32], [6 x i32]* %".5", i32 0, i32 4
  store i32 21, i32* %".14"
  %".16" = getelementptr [6 x i32], [6 x i32]* %".5", i32 0, i32 5
  store i32 67, i32* %".16"
  %".18" = alloca i32
  store i32 4, i32* %".18"
  %".20" = alloca i32
  store i32 0, i32* %".20"
  %".22" = alloca i32
  store i32 -1, i32* %".22"
  %".24" = load i32, i32* %".20"
  %".25" = icmp slt i32 %".24", 6
  %".26" = load i32, i32* %".22"
  %".27" = icmp eq i32 %".26", -1
  %".28" = and i1 %".25", %".27"
  br i1 %".28", label %"while_loop_entry_1", label %"while_loop_otherwise_1"
while_loop_entry_1:
  %".30" = load i32, i32* %".20"
  %".31" = getelementptr [6 x i32], [6 x i32]* %".5", i32 0, i32 %".30"
  %".32" = load i32, i32* %".31"
  %".33" = load i32, i32* %".18"
  %".34" = icmp eq i32 %".32", %".33"
  br i1 %".34", label %"while_loop_entry_1.if", label %"while_loop_entry_1.endif"
while_loop_otherwise_1:
  %".48" = load i32, i32* %".22"
  call void @"print_int"(i32 %".48")
  ret void
while_loop_entry_1.if:
  %".36" = load i32, i32* %".20"
  store i32 %".36", i32* %".22"
  br label %"while_loop_entry_1.endif"
while_loop_entry_1.endif:
  %".39" = load i32, i32* %".20"
  %".40" = add i32 %".39", 1
  store i32 %".40", i32* %".20"
  %".42" = load i32, i32* %".20"
  %".43" = icmp slt i32 %".42", 6
  %".44" = load i32, i32* %".22"
  %".45" = icmp eq i32 %".44", -1
  %".46" = and i1 %".43", %".45"
  br i1 %".46", label %"while_loop_entry_1", label %"while_loop_otherwise_1"
}

declare void @"print_int"(i32 %".1")
