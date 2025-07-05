#!/usr/bin/perl
use strict;
use warnings;

# Read all input
my $text = do { local $/; <STDIN> };

# Remove extra whitespace and newlines
$text =~ s/\s+/ /g;
$text =~ s/^\s+|\s+$//g;

# Split on sentence boundaries (period, exclamation, question mark)
# followed by whitespace and capital letter or end of string
my @sentences = split /([.!?])\s+(?=[A-Z]|$)/, $text;

# Reconstruct sentences with their punctuation
my @complete_sentences;
for (my $i = 0; $i < @sentences; $i += 2) {
    my $sentence = $sentences[$i];
    my $punct = $sentences[$i + 1] || '';
    
    if ($sentence =~ /\S/) {  # Only add non-empty sentences
        push @complete_sentences, $sentence . $punct;
    }
}

# Output one sentence per line
foreach my $sentence (@complete_sentences) {
    $sentence =~ s/^\s+|\s+$//g;  # Trim whitespace
    print "$sentence\n" if $sentence;
}
