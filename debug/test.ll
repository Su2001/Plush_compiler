
define void @"main"(i8** %"args")
{
main_entry:
  %".3" = alloca i8**
  store i8** %"args", i8*** %".3"
  %".5" = alloca i32
  store i32 7, i32* %".5"
  %".7" = alloca i1
  store i1 1, i1* %".7"
  %".9" = load i32, i32* %".5"
  %".10" = add i32 %".9", 3
  %".11" = alloca i32
  store i32 %".10", i32* %".11"
  ret void
}
