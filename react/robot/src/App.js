import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Grid from '@material-ui/core/Grid';
import Slider from '@material-ui/core/Slider';
import Switch from '@material-ui/core/Switch'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import TextField from "@material-ui/core/TextField";
import React from 'react';
import './App.css';
import ButtonCross from './ButtonCross';
import DirectionCross from "./DirectionCross";

class App extends React.Component {

  constructor(props){
    super(props);
    this.state = {
        camera_position_x: 0,
        camera_position_y: 0,
        left_on: false,
        left_color: 'white',
        right_on: false,
        right_color: 'white',
        speed: 80,
        duration: 0.5,
        elbow_angle: 90,
        claw_angle: 90
    };
  }

  componentDidMount() {
      let url = '/robot/status/';
      if(process.env.REACT_APP_API_URL) {
          url = process.env.REACT_APP_API_URL + url;
      }
      fetch(url)
          .then(response => response.json())
          .then(data => this.updateState(data))
          .catch((error) => {
            console.error('Error:', error);
          });
  }

  updateState = (data) => {
    this.setState({
        camera_position_x: data.robot.camera.position.x,
        camera_position_y: data.robot.camera.position.y,
        left_on: data.robot.led.state.left_on,
        left_color: data.robot.led.state.left_color,
        right_on: data.robot.led.state.right_on,
        right_color: data.robot.led.state.right_color,
        elbow_angle: data.robot.arm.elbow_angle,
        claw_angle: data.robot.arm.claw_angle
     });
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

  updateSpeed = (event, value) => {
    this.setState({
        speed: value
    })
  }

  updateDuration = (event, value) => {
    this.setState({
        duration: value
    })
  }

  switchFrontLight = (event, checked) => {
      this.setLedState (checked, this.state.left_color, checked, this.state.right_color);
  }

  switchFrontLightColor = (color) => {
      this.setLedState (this.state.left_on, color, this.state.right_on, color);
  }

  keyPress = (e) => {
      if(e.keyCode === 13 && e.target.value !== ""){
         this.saySomething( e.target.value)
          e.target.value = "";
      }
   }


  saySomething (text) {
      let url = '/robot/say/';
      if(process.env.REACT_APP_API_URL) {
          url = process.env.REACT_APP_API_URL + url;
      }
      fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text
        })
      })
      .then(response => response.json())
      .then(data => this.updateState(data))
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  setCameraPosition (pos_x, pos_y) {
      let url = '/robot/set_camera_position/';
      if(process.env.REACT_APP_API_URL) {
          url = process.env.REACT_APP_API_URL + url;
      }
      fetch(url, {
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
      .then(data => this.updateState(data))
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  moveRobot (direction, heading) {
      let url = '/robot/move/';
      if(process.env.REACT_APP_API_URL) {
          url = process.env.REACT_APP_API_URL + url;
      }
      fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            speed: this.state.speed,
            direction: direction,
            heading: heading,
            duration: this.state.duration
        })
      })
      .then(response => response.json())
      .then(data => this.updateState(data))
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  moveArm (elbow_angle, claw_angle) {
      let url = '/robot/move_arm/';
      if(process.env.REACT_APP_API_URL) {
          url = process.env.REACT_APP_API_URL + url;
      }
      fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            elbow_angle: elbow_angle,
            claw_angle: claw_angle
        })
      })
      .then(response => response.json())
      .then(data => this.updateState(data))
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  setLedState (left_on, left_color, right_on, right_color) {
      let url = '/robot/set_led_state/';
      if(process.env.REACT_APP_API_URL) {
          url = process.env.REACT_APP_API_URL + url;
      }
      fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            left_on: left_on,
            left_color: left_color,
            right_on: right_on,
            right_color: right_color,
        })
      })
      .then(response => response.json())
      .then(data => this.updateState(data))
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  render() {
      return (
        <div className="App">
          <header className="App-header">
             <Grid container spacing={0} direction="row" justify="center" alignItems="center">
                <Grid item xl={2} md={2} sm={2} xs={12}>
                    <p>
                        Camera: {this.state.camera_position_x}, {this.state.camera_position_y}
                    </p>
                    <ButtonCross
                         up_callback={this.cameraUp}
                         down_callback={this.cameraDown}
                         left_callback={this.cameraLeft}
                         right_callback={this.cameraRight}
                         center_callback={this.cameraCenter}/>
                    <Grid container spacing={2}>
                        <Grid item xl={12} md={12} sm={12} xs={12}>
                            <FormControlLabel control={<Switch onChange={this.switchFrontLight}/>} label="Front Light" />
                        </Grid>
                        <Grid item xl={1} md={1} sm={1} xs={1}/>
                        <Grid item xl={10} md={10} sm={10} xs={10}>
                            <Button
                                style={{backgroundColor: '#FFFFFF'}}
                                fullWidth
                                onClick={this.switchFrontLightColor.bind(this, "white")}
                            >
                                W
                            </Button>
                        </Grid>
                        <Grid item xl={1} md={1} sm={1} xs={1}/>
                        <Grid item xl={3} md={3} sm={3} xs={3}>
                            <Button
                                style={{backgroundColor: '#FF0000'}}
                                onClick={this.switchFrontLightColor.bind(this, "red")}
                            >
                                R
                            </Button>
                        </Grid>
                        <Grid item xl={1} md={1} sm={1} xs={1}/>
                        <Grid item xl={3} md={3} sm={3} xs={3}>
                            <Button
                                style={{backgroundColor: '#00FF00'}}
                                onClick={this.switchFrontLightColor.bind(this, "green")}
                            >
                                G
                            </Button>
                        </Grid>
                        <Grid item xl={1} md={1} sm={1} xs={1}/>
                        <Grid item xl={3} md={3} sm={3} xs={3}>
                            <Button
                                style={{backgroundColor: '#0000FF'}}
                                onClick={this.switchFrontLightColor.bind(this, "blue")}
                            >
                                B
                            </Button>
                        </Grid>
                        <Grid item xl={1} md={1} sm={1} xs={1}/>
                        <Grid item xl={3} md={3} sm={3} xs={3}>
                            <Button
                                style={{backgroundColor: '#00FFFF'}}
                                onClick={this.switchFrontLightColor.bind(this, "cyan")}
                            >
                                C
                            </Button>
                        </Grid>
                        <Grid item xl={1} md={1} sm={1} xs={1}/>
                        <Grid item xl={3} md={3} sm={3} xs={3}>
                            <Button
                                style={{backgroundColor: '#FF00FF'}}
                                onClick={this.switchFrontLightColor.bind(this, "pink")}
                            >
                                P
                            </Button>
                        </Grid>
                        <Grid item xl={1} md={1} sm={1} xs={1}/>
                        <Grid item xl={3} md={3} sm={3} xs={3}>
                            <Button
                                style={{backgroundColor: '#FFFF00'}}
                                onClick={this.switchFrontLightColor.bind(this, "yellow")}
                            >
                                Y
                            </Button>
                        </Grid>
                    </Grid>
                </Grid>
                <Grid item xl={6} md={6} sm={6} xs={12}>
                    <Grid item xl={12} md={12} sm={12} xs={12}>
                        <img src={(process.env.REACT_APP_API_URL ? process.env.REACT_APP_API_URL : "") + "/robot/stream/"} width="480" height="360" alt="Camera Feed"/>
                    </Grid>
                    <Grid item xl={12} md={12} sm={12} xs={12}>
                        <p>
                            Claw
                        </p>
                        <ButtonGroup variant="contained" aria-label="outlined primary button group">
                            <Button onClick={this.moveArm.bind(this, this.state.elbow_angle, 45)}>Open</Button>
                            <Button onClick={this.moveArm.bind(this, this.state.elbow_angle, 0)}>Close</Button>
                            <Button onClick={this.moveArm.bind(this, 90, 90)}>Park</Button>
                        </ButtonGroup>
                        <p>
                            Elbow Angle
                        </p>
                        <ButtonGroup variant="contained" aria-label="outlined primary button group">
                            <Button onClick={this.moveArm.bind(this, 0, this.state.claw_angle)}>0 (Down)</Button>
                            <Button onClick={this.moveArm.bind(this, 30, this.state.claw_angle)}>30</Button>
                            <Button onClick={this.moveArm.bind(this, 45, this.state.claw_angle)}>45</Button>
                            <Button onClick={this.moveArm.bind(this, 60, this.state.claw_angle)}>60</Button>
                            <Button onClick={this.moveArm.bind(this, 90, this.state.claw_angle)}>90 (Up)</Button>
                        </ButtonGroup>
                    </Grid>
                </Grid>
                <Grid item xl={3} md={3} sm={3} xs={12}>
                    <p>
                        Speed
                    </p>
                    <Slider
                        defaultValue={this.state.speed}
                        valueLabelDisplay="on"
                        min={0}
                        max={100}
                        onChange={this.updateSpeed}
                        aria-label="Speed Slider" />
                    <p>
                        Duration
                    </p>
                    <Slider
                        defaultValue={this.state.duration}
                        valueLabelDisplay="on"
                        min={0.2}
                        max={5}
                        step={0.1}
                        onChange={this.updateDuration}
                        aria-label="Duration Slider" />
                    <DirectionCross
                        forward_callback={this.moveRobot.bind(this, 'F', 0)}
                        forward_slight_left_callback={this.moveRobot.bind(this, 'F', 45)}
                        forward_left_callback={this.moveRobot.bind(this, 'F', 90)}
                        forward_slight_right_callback={this.moveRobot.bind(this, 'F', -45)}
                        forward_right_callback={this.moveRobot.bind(this, 'F', -90)}
                        backward_callback={this.moveRobot.bind(this, 'B', 0)}
                        backward_slight_left_callback={this.moveRobot.bind(this, 'B', 45)}
                        backward_left_callback={this.moveRobot.bind(this, 'B', 90)}
                        backward_slight_right_callback={this.moveRobot.bind(this, 'B', -45)}
                        backward_right_callback={this.moveRobot.bind(this, 'B', -90)}
                    />
                    <Grid container>
                        <Grid item xl={12} md={12} sm={12} xs={12}>
                            <p>
                                Say Something
                            </p>
                        </Grid>
                        <Grid item xl={12} md={12} sm={12} xs={12}>
                            <TextField onKeyDown={this.keyPress} fullWidth={true}/>
                        </Grid>
                    </Grid>
                </Grid>
                <Grid item xl={1} md={1} sm={1} xs={0}/>
            </Grid>
          </header>
        </div>
      );
  }
}

export default App;
