#!/usr/bin/perl -w
#
#	Converts data in a triple format "id1 id2 id3 target" (like often used in recommender systems for rating prediction) into the libfm format.
# 
#	Author:   Steffen Rendle, http://www.libfm.org/
#	modified: 2012-12-27
#
#	History
#		2012-12-27: header is not printed
#
#	Copyright 2010-2012 Steffen Rendle, see license.txt for more information

use Getopt::Long;
use strict;

srand();


my $file_in;
my $has_header = 0;
my $target_column = undef;
my $_delete_column = "";
my $offset = 0; # where to start counting for indices. For libsvm one should start with 1; libfm can deal with 0.
my $separator = " ";

# example
# ./triple_format_to_libfm.pl --in train.txt,test.txt --header 0 --target_column 2 --delete_column 3,4,5,6,7 --offset 0


GetOptions(
	'in=s'             => \$file_in,
	'header=i'	   => \$has_header,
	'target_column=i'  => \$target_column,
	'delete_column=s'  => \$_delete_column,
	'offset=i'         => \$offset,
	'separator=s'      => \$separator,
);

(defined $target_column) || die "no target column specified";

my @files = split(/[,;]/, $file_in);
my %delete_column;
foreach my $c (split(/[,;]/, $_delete_column)) {
	$delete_column{int($c)} = 1;
}

my %id;
my $id_cntr = $offset;


foreach my $file_name (@files) {
	my $file_out = $file_name . ".libfm";
	print "transforming file $file_name to $file_out...";
	my $num_triples = 0;

	open my $IN, '<' , $file_name;
	open my $OUT, '>' , $file_out;
	if ($has_header) {
		$_ = <$IN>;
#		print {$OUT} $_;
	}
	while (<$IN>) {
		chomp;
		if ($_ ne "") {
			my @data = split /$separator/;
			($#data >= $target_column) || die "not enough values in line $num_triples, expected at least $target_column values\nfound $_\n";
			my $out_str = $data[$target_column];
			my $out_col_id = 0; ## says which column in the input a field corresponds to after "deleting" the "delete_column", i.e. it is a counter over the #$data-field in @data assuming that some of the columns have been deleted; one can see this as the "group" id
			for (my $i = 0; $i <= $#data; $i++) {
				if (($i != $target_column) && (! exists $delete_column{$i})) {
					my $col_id = $out_col_id . " " . $data[$i]; ## this id holds the unique id of $data[$i] (also w.r.t. its group) 
					if (! exists $id{$col_id}) {
						$id{$col_id} = $id_cntr;
						$id_cntr++;
					}
					my $libfm_id = $id{$col_id};
					$out_str .= " " . $libfm_id . ":1";
					$out_col_id++;
				}
			}
			print {$OUT} $out_str, "\n";
		}
	}
	close $OUT;
	close $IN;
	print "\n";
}

