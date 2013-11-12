
@rem  The \gram\ directory including the grammars files is not specified here (it is in the tokenAndParse script)

@rem without log of rejected string
perl tokenAndParse.pl G=GramCROHMEpart2.xml F=listeTest.txt O=emAccepted_test.txt -L

@rem with log of rejected string
@rem perl tokenAndParse.pl G=GramCROHMEpart2.xml F=listeTest.txt O=emAccepted_test.txt

pause