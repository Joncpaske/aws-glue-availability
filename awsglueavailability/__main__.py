from awsglueavailability.client import Glue, EC2
from awsglueavailability.app import draw_diagram


draw_diagram(
    Glue(),
    EC2()
)