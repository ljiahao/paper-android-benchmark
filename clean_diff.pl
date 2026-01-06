use strict;
use warnings;

local $/;
my $t = <>;

# 1) booktabs rules 不要被 DIF...FL 包
$t =~ s/\\DIF(add|del)FL\{\\toprule\s*\}/\\toprule\n/g;
$t =~ s/\\DIF(add|del)FL\{\\midrule\s*\}/\\midrule\n/g;
$t =~ s/\\DIF(add|del)FL\{\\bottomrule\s*\}/\\bottomrule\n/g;

# 2) 修复 cmidrule 被拆参
$t =~ s/\\DIFaddFL\{\\cmidrule(\([^)]*\))\}\{\\DIFaddFL\{([^}]*)\}\}/\\cmidrule$1\{$2\}/g;
$t =~ s/\\DIFdelFL\{\\cmidrule(\([^)]*\))\}\{\\DIFdelFL\{([^}]*)\}\}/\\cmidrule$1\{$2\}/g;

# 3) 拆开 “\DIFaddFL{ \midrule <newline> TEXT }”
$t =~ s/\\DIFaddFL\{\\midrule\s*\n\s*([^}]*)\}/\\midrule\n\\DIFaddFL\{$1\}/g;
$t =~ s/\\DIFdelFL\{\\midrule\s*\n\s*([^}]*)\}/\\midrule\n\\DIFdelFL\{$1\}/g;

# 4) 删除单独一行的 "}"（修复 $\ 插值：不要写 $\n）
$t =~ s/^\s*\}\s*\n//mg;

print $t;