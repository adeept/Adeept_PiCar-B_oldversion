import Grid from '@material-ui/core/Grid';
import IconButton from '@material-ui/core/IconButton';
import ArrowUpwardIcon from '@material-ui/icons/ArrowUpward';
import ArrowDownwardIcon from '@material-ui/icons/ArrowDownward';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import ArrowForwardIcon from '@material-ui/icons/ArrowForward';
import CenterFocusStrongIcon from '@material-ui/icons/CenterFocusStrong';
import React from 'react';

class ButtonCross extends React.Component {

    render() {
        return (
          <Grid container>
            <Grid item xs={5}>
            </Grid>
            <Grid item xs={2}>
              <IconButton onClick={this.props.up_callback}><ArrowUpwardIcon/></IconButton>
            </Grid>
            <Grid item xs={5}>
            </Grid>


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


            <Grid item xs={5}>
            </Grid>
            <Grid item xs={2}>
              <IconButton onClick={this.props.down_callback}><ArrowDownwardIcon/></IconButton>
            </Grid>
            <Grid item xs={5}>
            </Grid>
            <Grid item xs={3}>
            </Grid>
          </Grid>
          )
    }
}

export default ButtonCross;
