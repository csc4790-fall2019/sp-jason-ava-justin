import React from 'react';
import Chart from 'react-google-charts';
import Button from 'react-bootstrap/Button';
import {
  Box,
  Card,
  Image,
  Heading,
  Text
} from 'rebass'

export default class Display extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      graphdata: ['null','null'],
      polScore: -999,
      datapoints: [],
      ticker: 'TSLA',
      month: 8,
      lowstock:99999,
      highstock:-99999
    }
  }

  getStockData = () => {
    try{
      (async () => {
        const stockresponse = await fetch('http://127.0.0.1:5000/api/stockdata/'+this.state.ticker+'/8',{
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
         }
        });

        const polarityresponse = await fetch('http://127.0.0.1:5000/api/polarity/'+this.state.ticker+'/2019-08-01/2019-08-31',{
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        });

        var polarityres = await polarityresponse.json();
        polarityres = polarityres.PolarityScores;
        var stockres = await stockresponse.json();
        stockres = stockres.Stockdata;

        var set = new Set();

        this.setState({
          lowstock:99999,
          highstock:-99999
        })

        var stockmap = new Map();
        stockres.forEach((element) => {
          set.add(element[0]);
          stockmap.set(element[0],element[1])

          if(element[1]>this.state.highstock)
            this.setState({
              highstock: element[1]
            })

          if(element[1]<this.state.lowstock)
            this.setState({
              lowstock: element[1]
            })
        })

        var polaritymap = new Map();
        polarityres.forEach((element) => {
          set.add(element[0])
          polaritymap.set(element[0],element[1])
        })

        var graphdata = [];
        set.forEach((entry) => {graphdata.push([entry,0,0])})

        graphdata.forEach((point, index) => {
          debugger
          if(stockmap.get(point[0]) !== undefined)
            point[1] = stockmap.get(point[0])

          if(polaritymap.get(point[0]) !== undefined){
              var pol = polaritymap.get(point[0])
              pol = (pol + 1)*(this.state.highstock-this.state.lowstock)/2+this.state.lowstock
              point[2]= pol;
            }
           else if(index !== 0 ){
            graphdata[index][2] = graphdata[index-1][2]
           }
           else{
             graphdata[index][2] = (this.state.highstock-this.state.lowstock)/2 + this.state.lowstock
           }
        })

        graphdata.pop(); //DELETE THIS LATER THIS IS JUST FOR DEMO
        graphdata.pop();
        graphdata.unshift(['x',this.state.ticker,'polarity'])

        console.log(JSON.stringify(stockres))
        console.log(JSON.stringify(polarityres))
        console.log(graphdata);

        this.setState({
          graphdata: graphdata,
        });

      })()
    }catch(err){
      console.log(err)
    }
  }

  componentDidMount() {
    this.getStockData();
  }

  handleTickerSubmit = (event) => {
    this.getStockData()
    event.preventDefault();
  }

  handleChange = (event) => {
    this.setState({
      ticker: event.target.value
    })
  }

  render(){
    var data = this.state.graphdata;

    return(
      <div>
        <Box width = {3/4}
          sx = {{
            mx: 'auto'
          }}>
          <Card
            sx = {{
              my: 3
            }}>
            <Heading
              fontSize={[ 5, 6, 7 ]}
              color='primary'>
              Sentiment Analysis vs. Equity Price History
            </Heading>
          </Card>

          <Card
            sx = {{
              my: 3
            }}>
            <form onSubmit={this.handleTickerSubmit}>
              <label>
                Pick a company:
                <select value={this.state.ticker} onChange={this.handleChange}>
                  <option value="TSLA">Tesla</option>
                  <option value="AAPL">Apple</option>
                  <option value="GOOGL">Google</option>
                  <option value="MSFT">Microsoft</option>
                  <option value="FB">Facebook</option>
                </select>
              </label>
              <input type="submit" value="Submit" />
            </form>
          </Card>
          <Card
            sx = {{
              mx: 'auto',
              my: 3
            }}>
            <Chart
              //width={'600px'}
              height={'600px'}
              chartType="LineChart"
              loader={<div>Loading Chart</div>}
              data={data}
              options={{
                hAxis: {
                  title: 'Date',
                },
                vAxis: {
                  title: 'Price',
                },
                animation: {
                  duration: 1000,
                  easing: 'out',
                  startup: true,
                },
              }}
              rootProps={{ 'data-testid': '1' }}
            />
          </Card>
        </Box>
      </div>
    );
  }

}
