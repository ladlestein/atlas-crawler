#!/bin/bash

SGINFO="$HOME/Downloads/sginfo_1_01_mac_10.4_intel.exe"

call_sginfo() {

    for i in {1..230}
    do
        $SGINFO $i
    done

}

extract_data() {
    echo "["
    gawk '/Space Group/ { number = gensub(/([0-9]+):?.*/, "\\1", "g", $3) }; /Order +[0-9]+/ { print "{ group:", number, "order:", $2, "}" }'
    echo "]"
}

call_sginfo | extract_data

