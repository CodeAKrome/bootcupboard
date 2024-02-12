#!env perl
$p = $ARGV[0];
$t = 0;

while (<STDIN>) {

    if (/$p/) {
	$t = 1;
    }

    if ($t) {
	print;
    }
}

    
