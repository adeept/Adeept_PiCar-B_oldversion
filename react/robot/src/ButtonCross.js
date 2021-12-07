import Grid from '@material-ui/core/Grid';
import IconButton from '@material-ui/core/IconButton';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import ArrowForwardIcon from '@material-ui/icons/ArrowForward';
import CenterFocusStrongIcon from '@material-ui/icons/CenterFocusStrong';
import React from 'react';

class ButtonCross extends React.Component {

    render() {
        return (
          <Grid container>


            <Grid item xs={3}>
            </Grid>
            <Grid item xs={2}>
              <IconButton onClick={this.props.left_callback}><ArrowBackIcon/></IconButton>
            </Grid>
            <Grid item xs={2}>
              <IconButton onClick={this.props.center_callback}><CenterFocusStrongIcon/></IconButton>
            </Grid>
            <Grid item xs={2}>
              <IconButton onClick={this.props.right_callback}><ArrowForwardIcon/></IconButton>
            </Grid>
            <Grid item xs={3}>
            </Grid>


            <Grid item xs={3}>
            </Grid>
          </Grid>
          )
    }
}

export default ButtonCross;
