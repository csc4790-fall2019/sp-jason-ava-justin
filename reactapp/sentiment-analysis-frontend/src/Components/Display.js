import React from 'react';
import Chart from 'react-google-charts';

export default class Display extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      response: ['null','null'],
      polScore: -999,
      datapoints: []
    }
  }

  componentDidMount() {
    try{
      (async () => {
        const response = await fetch('http://127.0.0.1:5000/api/stockdata/TSLA/8',{
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
         }
        });
        const res = await response.json()
        console.log(JSON.stringify(res))
        debugger;
        this.setState({
          response: res.Stockdata,
          //polScore: res.polScore
        });
        console.log(this.state.response)
      })()
    }catch(err){
      console.log(err)
    }


  }

  render(){
    var data = this.state.response;
    if(data.length > 1)
      data.unshift(['x','TSLA'])
    debugger;
    return(
      <div>
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
