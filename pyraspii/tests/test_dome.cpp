#include <catch.hpp>
#include "rasp_master.hpp"

TEST_CASE("pydome send and receive")
{
    REQUIRE(send_data(0, 0x44) == 0);
    REQUIRE(getData_from(0x44) == 0);
}
