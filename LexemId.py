TStart = -1
TId = 0
TNum10 = 1
TNum16 = 2
TInt = 3
TShort = 4
TLong = 5
TDo = 6
TWhile = 7
TMain = 8
TReturn = 9
TOpen = 10
TClose = 11
TOpenFigure = 12
TCloseFigure = 13
TPlus = 14
TMinus = 15
TPlusPlus = 16
TMinusMinus = 17
TDiv = 18
TMod = 19
TMul = 20
TGreater = 21
TLess = 22
TGreaterEq = 23
TLessEq = 24
TEq = 25
TUnEq = 26
TAssign = 27
TPlusAssign = 28
TMinusAssign = 29
TDivAssign = 30
TModAssign = 21
TMulAssign = 32
TComma = 33
TSemicolon = 34
TError = 35
TEndFile = 36

lexemIdToStr = {TId: "identifier", TNum10: "decimal", TNum16: "hex", TInt: "int",
                TShort: "short", TLong: "long", TDo: "do", TWhile: "while",
                TReturn: "return", TMain: "main", TOpen: "(", TClose: ")",
                TOpenFigure: "{", TCloseFigure: "}", TPlus: "+", TMinus: "-",
                TPlusPlus: "++", TMinusMinus: "--", TDiv: "/", TMod: "%", TMul: "*",
                TGreater: ">", TLess: "<", TGreaterEq: ">=", TLessEq: "<=", TEq: "==",
                TUnEq: "!=", TAssign: "=", TPlusAssign: "+=", TMinusAssign: "-=",
                TDivAssign: "/=", TModAssign: "%=", TMulAssign: "*=", TComma: ",",
                TSemicolon: ";", TError: "error", TEndFile: "end file"}

keyWords = {TDo: "do", TReturn: "return", TWhile: "while", TShort: "short", TInt: "int", TLong: "long"}
