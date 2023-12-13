var api = 'http://127.0.0.1:5000/api/calorieLog'; //api for calorie logs

/// The API will only contain details of the logged in user
/// graph will be drawn based on users' info 
/////////////////////////////////////////////////////////////////////////////////////
/// ideally, if admin@fitwell.com logs in, 
/// admin would be able to see all data of users being presented in different lines
/// however, not enough time to figure this part out. 
/// I also did not want to use other methods as 
/// it is waste if this API function was not used 
/////////////////////////////////////////////////////////////////////////////////////
/// Currently, when admin logs in, all data will be stored in the API
/// unfortunately, all data will be messed up together

function parseData(data){
  var arr = []; //creates empty array

  debugger
  for (var calorieLog of data.calorieLogs) {
      arr.push( 
        { date: Date.parse(calorieLog.datetime), // get date 
          value: +calorieLog.calorie //to change calorie string into values  
        });
  }
  return arr;
}

fetch(api)
  .then((response) => {
        return response.json();
    })
    .then((data) => {
        var parsedData = parseData(data);
        drawChart(parsedData);
    });

function drawChart(data) {

    debugger
    // to set dimensions of graph
    var margin = {top: 10, right: 30, bottom: 90, left: 60},
        width = 680 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
  
    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")")
    
    debugger 
    var x = d3.scaleTime()
      .domain(d3.extent(data, function(d) { return d.date; }))
      .range([ 0, width ]);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%m-%d")))
      .selectAll("text")	
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
      .attr("transform", "rotate(-65)");
  
    debugger
    var y = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) { return +d.value+100; })])
      .range([ height, 0 ]);
    svg.append("g")
      .call(d3.axisLeft(y));

    // // Add the line
    // svg.append("path")
    //   .datum(data)
    //   .attr("fill", "none")
    //   .attr("stroke", "steelblue")
    //   .attr("stroke-width", 1.5)
    //   .attr("d", d3.line()
    //     .x(function(d) { return x(d.date) })
    //     .y(function(d) { return y(d.value) })
    //     )

    // Replace the existing line path with a curved line path
    svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .attr("d", d3.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.value); })
      .curve(d3.curveBasis) // Use curveBasis interpolation
      )

  }

