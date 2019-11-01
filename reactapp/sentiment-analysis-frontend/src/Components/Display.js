import React from 'react';
import Chart from 'react-google-charts';
import Button from 'react-bootstrap/Button';

export default class Display extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      response: ['null','null'],
      polScore: -999,
      datapoints: [],
      ticker: 'TSLA',
      month: 8
    }
  }

  getStockData = () => {
    try{
      (async () => {
        console.log(this.state.ticker)
        const response = await fetch('http://127.0.0.1:5000/api/stockdata/'+this.state.ticker+'/8',{
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
         }
        });
        const res = await response.json()
        res.Stockdata.unshift(['x',this.state.ticker])
        console.log(JSON.stringify(res))
        this.setState({
          response: res.Stockdata,
        });
        console.log(this.state.response)
      })()
    }catch(err){
      console.log(err)
    }
  }

  componentDidMount() {
    this.getStockData();
  }

  // componentDidUpdate() {
  //   this.getStockData();
  // }

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
    var data = this.state.response;

    return(
      <div>
        <form onSubmit={this.handleTickerSubmit}>
          <label>
            Pick a company:
            <select value={this.state.ticker} onChange={this.handleChange}>
              <option value="TSLA">Tesla</option>
              <option value="AAPL">Apple</option>
              <option value="GOOGL">Google</option>
              <option value="MSFT">Microsoft</option>
            </select>
          </label>
          <input type="submit" value="Submit" />
        </form>
        <Chart
          width={'600px'}
          height={'400px'}
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
          }}
          rootProps={{ 'data-testid': '1' }}
        />
      </div>
    );
  }

}
