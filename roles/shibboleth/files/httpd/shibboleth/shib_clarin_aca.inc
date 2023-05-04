#Setting to allow access for 'academic' users Included in shib.conf
# member is ok
Require shib-attr unscoped-affiliation ~ member student faculty

#scoped ok, if not followed by @clarin.
# Note: Rewrite this, when moving to 2.4! 
Require shib-attr affiliation ~ member@[^c] member@c[^l] member@cl[^a] member@cla[^r] member@clar[^i] member@clari[^n] member@clarin[^\.]  student faculty
# clarin.eu
Require shib-attr entitlement ~ http://www.clarin.eu/entitlement/academic 
# LBR ACA status will always work
Require shib-attr entitlement ~ urn:nbn:fi:lb-2016110710@LBR
