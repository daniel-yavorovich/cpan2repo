#!/usr/bin/perl
use Module::CoreList ();

$num_args = $#ARGV + 1;
if ($num_args != 1) {
  print "Usage: check_core_module.pl cpan_name\n";
  exit;
}

sub is_core_module {
    my ( $module, $ver ) = @_;

    my $v = Module::CoreList->first_release($module, $ver);   # 5.009002

    return unless defined $v;

    $v = version->new($v);                              # v5.9.2
    ( $v = $v->normal ) =~ s/^v//;                      # "5.9.2"

    return $v;
}

if ( is_core_module( $ARGV[0]) ) {
        die $ARGV[0]
                . " is a standard module."
}