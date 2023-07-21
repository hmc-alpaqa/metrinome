; ModuleID = '/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/fib_rec_wrapper_fib_rec_wrapper_.bc'
source_filename = "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/fib_rec_wrapper_fib_rec_wrapper_.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [33 x i8] c"e5884fafa80d470982432cd3b1f08a20\00", align 1

; Function Attrs: noinline nounwind uwtable
define i32 @fib_rec(i32) #0 !dbg !7 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !12, metadata !DIExpression()), !dbg !13
  %6 = load i32, i32* %3, align 4, !dbg !14
  %7 = icmp sle i32 %6, 1, !dbg !16
  %8 = load i32, i32* %3, align 4
  br i1 %7, label %9, label %10, !dbg !17

; <label>:9:                                      ; preds = %1
  store i32 %8, i32* %2, align 4, !dbg !18
  br label %19, !dbg !18

; <label>:10:                                     ; preds = %1
  call void @llvm.dbg.declare(metadata i32* %4, metadata !20, metadata !DIExpression()), !dbg !22
  %11 = sub nsw i32 %8, 1, !dbg !23
  %12 = call i32 @fib_rec(i32 %11), !dbg !24
  store i32 %12, i32* %4, align 4, !dbg !22
  call void @llvm.dbg.declare(metadata i32* %5, metadata !25, metadata !DIExpression()), !dbg !26
  %13 = load i32, i32* %3, align 4, !dbg !27
  %14 = sub nsw i32 %13, 2, !dbg !28
  %15 = call i32 @fib_rec(i32 %14), !dbg !29
  store i32 %15, i32* %5, align 4, !dbg !26
  %16 = load i32, i32* %4, align 4, !dbg !30
  %17 = load i32, i32* %5, align 4, !dbg !31
  %18 = add nsw i32 %16, %17, !dbg !32
  store i32 %18, i32* %2, align 4, !dbg !33
  br label %19, !dbg !33

; <label>:19:                                     ; preds = %10, %9
  %20 = load i32, i32* %2, align 4, !dbg !34
  ret i32 %20, !dbg !34
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: noinline nounwind uwtable
define i32 @fib_rec_wrapper(i32) #0 !dbg !35 {
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  call void @llvm.dbg.declare(metadata i32* %2, metadata !36, metadata !DIExpression()), !dbg !37
  %3 = load i32, i32* %2, align 4, !dbg !38
  %4 = call i32 @fib_rec(i32 %3), !dbg !39
  ret i32 %4, !dbg !40
}

; Function Attrs: noinline nounwind uwtable
define i32 @main() #0 !dbg !41 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  call void @llvm.dbg.declare(metadata i32* %2, metadata !44, metadata !DIExpression()), !dbg !45
  %3 = bitcast i32* %2 to i8*, !dbg !46
  call void @klee_make_symbolic(i8* %3, i64 4, i8* getelementptr inbounds ([33 x i8], [33 x i8]* @.str, i32 0, i32 0)), !dbg !47
  %4 = load i32, i32* %2, align 4, !dbg !48
  %5 = icmp slt i32 %4, -1, !dbg !50
  %6 = load i32, i32* %2, align 4, !dbg !51
  %7 = icmp sgt i32 %6, 1024, !dbg !52
  %or.cond = or i1 %5, %7, !dbg !53
  br i1 %or.cond, label %8, label %9, !dbg !53

; <label>:8:                                      ; preds = %0
  store i32 0, i32* %1, align 4, !dbg !54
  br label %12, !dbg !54

; <label>:9:                                      ; preds = %0
  %10 = load i32, i32* %2, align 4, !dbg !56
  %11 = call i32 @fib_rec_wrapper(i32 %10), !dbg !57
  store i32 %11, i32* %1, align 4, !dbg !58
  br label %12, !dbg !58

; <label>:12:                                     ; preds = %9, %8
  %13 = load i32, i32* %1, align 4, !dbg !59
  ret i32 %13, !dbg !59
}

declare void @klee_make_symbolic(i8*, i64, i8*) #2

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 6.0.1-10 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2)
!1 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/fib_rec_wrapper_fib_rec_wrapper_.c", directory: "/app/code")
!2 = !{}
!3 = !{i32 2, !"Dwarf Version", i32 4}
!4 = !{i32 2, !"Debug Info Version", i32 3}
!5 = !{i32 1, !"wchar_size", i32 4}
!6 = !{!"clang version 6.0.1-10 (tags/RELEASE_601/final)"}
!7 = distinct !DISubprogram(name: "fib_rec", scope: !8, file: !8, line: 4, type: !9, isLocal: false, isDefinition: true, scopeLine: 5, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!8 = !DIFile(filename: "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/cFiles/fib_rec_wrapper.c", directory: "/app/code")
!9 = !DISubroutineType(types: !10)
!10 = !{!11, !11}
!11 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!12 = !DILocalVariable(name: "n", arg: 1, scope: !7, file: !8, line: 4, type: !11)
!13 = !DILocation(line: 4, column: 17, scope: !7)
!14 = !DILocation(line: 6, column: 9, scope: !15)
!15 = distinct !DILexicalBlock(scope: !7, file: !8, line: 6, column: 9)
!16 = !DILocation(line: 6, column: 11, scope: !15)
!17 = !DILocation(line: 6, column: 9, scope: !7)
!18 = !DILocation(line: 7, column: 9, scope: !19)
!19 = distinct !DILexicalBlock(scope: !15, file: !8, line: 6, column: 17)
!20 = !DILocalVariable(name: "a", scope: !21, file: !8, line: 9, type: !11)
!21 = distinct !DILexicalBlock(scope: !15, file: !8, line: 8, column: 12)
!22 = !DILocation(line: 9, column: 13, scope: !21)
!23 = !DILocation(line: 9, column: 27, scope: !21)
!24 = !DILocation(line: 9, column: 17, scope: !21)
!25 = !DILocalVariable(name: "b", scope: !21, file: !8, line: 10, type: !11)
!26 = !DILocation(line: 10, column: 13, scope: !21)
!27 = !DILocation(line: 10, column: 25, scope: !21)
!28 = !DILocation(line: 10, column: 27, scope: !21)
!29 = !DILocation(line: 10, column: 17, scope: !21)
!30 = !DILocation(line: 11, column: 16, scope: !21)
!31 = !DILocation(line: 11, column: 20, scope: !21)
!32 = !DILocation(line: 11, column: 18, scope: !21)
!33 = !DILocation(line: 11, column: 9, scope: !21)
!34 = !DILocation(line: 13, column: 1, scope: !7)
!35 = distinct !DISubprogram(name: "fib_rec_wrapper", scope: !8, file: !8, line: 15, type: !9, isLocal: false, isDefinition: true, scopeLine: 15, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!36 = !DILocalVariable(name: "n", arg: 1, scope: !35, file: !8, line: 15, type: !11)
!37 = !DILocation(line: 15, column: 25, scope: !35)
!38 = !DILocation(line: 16, column: 20, scope: !35)
!39 = !DILocation(line: 16, column: 12, scope: !35)
!40 = !DILocation(line: 16, column: 5, scope: !35)
!41 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 4, type: !42, isLocal: false, isDefinition: true, scopeLine: 4, isOptimized: false, unit: !0, variables: !2)
!42 = !DISubroutineType(types: !43)
!43 = !{!11}
!44 = !DILocalVariable(name: "n", scope: !41, file: !1, line: 6, type: !11)
!45 = !DILocation(line: 6, column: 6, scope: !41)
!46 = !DILocation(line: 7, column: 21, scope: !41)
!47 = !DILocation(line: 7, column: 2, scope: !41)
!48 = !DILocation(line: 8, column: 7, scope: !49)
!49 = distinct !DILexicalBlock(scope: !41, file: !1, line: 8, column: 6)
!50 = !DILocation(line: 8, column: 8, scope: !49)
!51 = !DILocation(line: 8, column: 17, scope: !49)
!52 = !DILocation(line: 8, column: 18, scope: !49)
!53 = !DILocation(line: 8, column: 13, scope: !49)
!54 = !DILocation(line: 9, column: 4, scope: !55)
!55 = distinct !DILexicalBlock(scope: !49, file: !1, line: 8, column: 26)
!56 = !DILocation(line: 10, column: 25, scope: !41)
!57 = !DILocation(line: 10, column: 9, scope: !41)
!58 = !DILocation(line: 10, column: 2, scope: !41)
!59 = !DILocation(line: 11, column: 1, scope: !41)
