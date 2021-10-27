import Grid from '@material-ui/core/Grid';
import React from 'react';
import './App.css';
import ButtonCross from './ButtonCross';

class App extends React.Component {

  constructor(props){
    super(props);
    this.state = {
        camera_position_x: 0,
        camera_position_y: 0
    };
  }

  componentDidMount() {
    fetch('http://robot.local:8000/robot/status/')
          .then(response => response.json())
          .then(data => this.setState({
            camera_position_x: data.robot.camera.position.x,
            camera_position_y: data.robot.camera.position.y
          }));
  }

  cameraUp = () => {
    this.setCameraPosition(this.state.camera_position_x, this.state.camera_position_y + 5);
  }

  cameraDown = () => {
    this.setCameraPosition(this.state.camera_position_x, this.state.camera_position_y - 5);
  }

  cameraLeft = () => {
    this.setCameraPosition(this.state.camera_position_x + 5, this.state.camera_position_y);
  }

  cameraRight = () => {
    this.setCameraPosition(this.state.camera_position_x - 5, this.state.camera_position_y);
  }

  cameraCenter = () => {
    this.setCameraPosition(0, 0);
  }

  setCameraPosition (pos_x, pos_y) {
      fetch('http://robot.local:8000/robot/set_camera_position/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          x: pos_x,
          y: pos_y
        })
      })
      .then(response => response.json())
      .then(data => this.setState({
        camera_position_x: data.robot.camera.position.x,
        camera_position_y: data.robot.camera.position.y
      }));
  }

  render() {
      return (
        <div className="App">
          <header className="App-header">
             <Grid container spacing={0} direction="row" justify="center" alignItems="center">
                <Grid item xl={6} md={6} sm={6} xs={12}>
                    <img src="http://robot.local:8000/robot/stream/" width="480" height="360" alt="camera"/>
                </Grid>
                <Grid item xl={6} md={6} sm={6} xs={12}>
                    <p>
                        Camera: {this.state.camera_position_x}, {this.state.camera_position_y}
                    </p>
                    <ButtonCross
                     up_callback={this.cameraUp}
                     down_callback={this.cameraDown}
                     left_callback={this.cameraLeft}
                     right_callback={this.cameraRight}
                     center_callback={this.cameraCenter}/>
                </Grid>
            </Grid>
          </header>
        </div>
      );
  }
}

export default App;
