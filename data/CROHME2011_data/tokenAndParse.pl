#!perl
#Author : Harold Mouchère / IRCCyN / Universtié de Nantes

$GRAM = "GramCROHMEpart2.xml";

$fileToTest = "listeTest.txt";

$fileOutAccepted = "emAccepted.txt";

$withLog = "";

if($#ARGV == -1){
	print "options : tokenAndParse.pl G=grammar.xml F=listOfEmToTest.txt  O=AcceptedEm.txt\n";
	exit(-1);
}
foreach $p (@ARGV){
	if($p =~ /G=(.*)/){
		$GRAM = $1;
	}
	if($p =~ /F=(.*)/){
		$fileToTest = $1;
	}
	if($p =~ /O=(.*)/){
		$fileOutAccepted = $1;
	}	
	if($p =~ /-L/){
		$withLog = "\>\> emParse.log";
	}	
}

print " used grammar : $GRAM\n";
print " used list of EM : $fileToTest\n";
print " used output file : $fileOutAccepted\n";

open(EMLISTE,$fileToTest) || die "Impossible d'ouvrir le fichier $1 : $!";
open(OUTEMACC,">$fileOutAccepted");
open(OUTEMREJ,">emRejected.txt");
while($ligne = <EMLISTE>){ # pour chaque ligne
	if(not ($ligne =~ /^%/)){
		$original = $ligne;
		$ligne =~ s/[\r\n]//g; #chomp($ligne);
		#suppression des trucs encombrants
		$ligne =~ s/(\\ |\\,|\\;|\\>|\\!)/ /g; #supprime tous les espaces spéciaux	
		$ligne =~ s/\$/ /g; #les balises $ $ 
		$ligne =~ s/([^\\])([\}\{])/$1 $2 /g; #des acolades de priorité et fonctions spéciales mais différentes des \{ et \}
		$ligne =~ s/([^\\])([\}\{])/$1 $2 /g; #twice to deal with {{{{}}}} strings
		# séparations des symboles
		$ligne =~ s/([_\^+\-\*0-9=\/~,'\[\];:!\.><])/ $1 /g;#séparation des principaux symbole de 1 caractère
		$ligne =~ s/(\\?\|)/ $1 /g; #séparation des | et \|
		$ligne =~ s/(\\?[\(\)])/ $1 /g; #séparation des () et \(\)
		
		$ligne =~ s/(\\[A-Za-z]+)/ $1 /g; #séparation des macro
		$ligne =~ s/(\\[\}\{\(\)])/ $1 /g; #séparation des parenthèses spéciales
		$ligne =~ s/^([A-Za-z])([A-Za-z])/$1 $2 /g; #séparation lettres qui ne sont pas des macro au début de la chaine
		while($ligne =~ / [A-Za-z][A-Za-z]+/){ # while there are consecutive letters not starting  by a macro
			$ligne =~ s/ ([A-Za-z])([A-Za-z])/ $1 $2 /g; #séparation lettres qui ne sont pas des macro
			#print  $ligne."\n";
		}
		open(TEMPEM,">tempToken.txt");
		print TEMPEM $ligne;
		#print  $ligne."\n";
		close(TEMPEM);
		$res = `java -jar pep.jar -g gram/$GRAM -s S -v 0 - < tempToken.txt`;
		print $res;
		if($res =~/ACCEPT/){
			print OUTEMACC $original;
			if($withLog){
				$res =~/\(([0-9]*)\)/;
				if($1 gt 1){
					`java -jar pep.jar -g gram/$GRAM -s S -v 2 - < tempToken.txt $withLog`;
				}
			}
		}elsif($res =~/REJECT/){
			print OUTEMREJ $original;
			if($withLog){
				`java -jar pep.jar -g gram/$GRAM -s S -v 2 - < tempToken.txt $withLog`;
			}
		}else{
			print OUTEMREJ "ERROR :".$original."\n>>>".$res;
		}
	}
}

close(OUTEMACC);
close(OUTEMREJ);
close(EMLISTE);