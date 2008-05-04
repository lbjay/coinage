#!/usr/bin/perl

use strict;
use warnings;
use Log::Log4perl qw(:easy);
use Data::Dumper;

my %SITE_PORTS = (
    8085    => 'webridge',
    8084    => 'canary',
    8083    => 'prola',
    8082    => 'citebase',
    8081    => 'hubmed',
    );

my $port = $ENV{SERVER_PORT};
my $site = $SITE_PORTS{$port};

Log::Log4perl->easy_init({ 
    level   => $INFO,
    file    => ">>/var/www/coinage/ext_filter.log",
    });

my ($service) = @ARGV;
INFO "Site: $site, Service: $service";
#INFO Dumper(\%ENV);

my $baseurl = 'http://coinage.reallywow.com';
my $scripttag = qq|<script type="text/javascript" src="$baseurl/$service/engine?site=$site"></script>\n|;
my $coins = ($site eq 'webridge')
    ? '<span class="Z3988" title="ctx_ver=Z39.88-2004&' . $ENV{QUERY_STRING} . '"></span>'
    : '';

while (<stdin>) {
    s#(</body>)#$scripttag$1#iog;
    s#(<p class="wbIndCitation">)#$coins$1#iog;
    s#(?:<a href="http://worldcat.+</a>)##i;
    print;
}

exit 0;
