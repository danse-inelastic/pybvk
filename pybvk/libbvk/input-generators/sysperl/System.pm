package System;

sub modAxial { my ($R,$K,$Cb)=@_;  #  
  my $RdotR=$R->[0]*$R->[0]+$R->[1]*$R->[1]+$R->[2]*$R->[2];
  my $result=[@$R];
  foreach my $i (0..2) { foreach my $j (0..2) {
    push @$result, (($R->[$i]*$R->[$j]/$RdotR) * $K) +
                   ($i==$j?$Cb->[$i]:0);
  } }
  return @$result;
}

sub axial { my ($R,$r,$t)=@_;
  my $RdotR=$R->[0]*$R->[0]+$R->[1]*$R->[1]+$R->[2]*$R->[2];
  my $result=[@$R];
  foreach my $i (0..2) { foreach my $j (0..2) {
    push @$result, (($R->[$i]*$R->[$j]/$RdotR) * ($r-$t)) +
                   ($i==$j?$t:0);
  } }
  return @$result;
}

sub write { my ($cell,$atoms,$sites,$bonds,$symfile)=@_;
#  printf("Cell:\n");
#  printf("  %le %le %le\n",$cell->[0+0],$cell->[0+1],$cell->[0+2]);
#  printf("  %le %le %le\n",$cell->[3+0],$cell->[3+1],$cell->[3+2]);
#  printf("  %le %le %le\n",$cell->[6+0],$cell->[6+1],$cell->[6+2]);

  use IO::File;

  my $io=new IO::File("<syms/".$symfile);
  my $syms;
  $io->sysread($syms,1024*1024);
  $io->close;
  my $ns=unpack("i",substr($syms,0,4,""));
  printf("%d syms in %d bytes\n",$ns,length($syms));

  $io=new IO::File(">system");
  $io->syswrite(pack("i4",scalar(@$atoms),scalar(@$sites),scalar(@$bonds),$ns));
  $io->syswrite(pack("d9",@$cell));
  foreach my $a (@$atoms) { $io->syswrite(pack("a64d",@$a)); }
  foreach my $s (@$sites) { $io->syswrite(pack("d3i2",@$s,0)); }
  foreach my $b (@$bonds) { $io->syswrite(pack("i2d3d9",@$b)); }
  $io->syswrite($syms);
  $io->close;
}

1;
