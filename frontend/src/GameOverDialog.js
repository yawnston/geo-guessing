import React from "react";
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Typography from '@mui/material/Typography';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
    '& .MuiDialogContent-root': {
        padding: theme.spacing(2),
    },
    '& .MuiDialogActions-root': {
        padding: theme.spacing(1),
    },
}));

const BootstrapDialogTitle = (props) => {
    const { children, onClose, ...other } = props;

    return (
        <DialogTitle sx={{ m: 0, p: 2 }} {...other}>
            {children}
            {onClose ? (
                <IconButton
                    aria-label="close"
                    onClick={onClose}
                    sx={{
                        position: 'absolute',
                        right: 8,
                        top: 8,
                        color: (theme) => theme.palette.grey[500],
                    }}
                >
                    <CloseIcon />
                </IconButton>
            ) : null}
        </DialogTitle>
    );
};

export default function GameOverDialog(props) {
    const [open, setOpen] = React.useState(true);

    const handleClose = () => {
        setOpen(false);
        props.onNewGame();
        setOpen(true);
    };

    let dialogTitle = "";
    if (props.playerScoreTotal > props.aiScoreTotal) {
        dialogTitle = "You won! Congratulations!";
    } else if (props.playerScoreTotal < props.aiScoreTotal) {
        dialogTitle = "You lost, better luck next time.";
    } else {
        dialogTitle = "It's a tie! That's quite rare!";
    }
    return props.isGameOver === false ? null : (
        <div>
            <BootstrapDialog
                aria-labelledby="customized-dialog-title"
                open={open}
                disableEscapeKeyDown={true}
            >
                <BootstrapDialogTitle id="customized-dialog-title">
                    {dialogTitle}
                </BootstrapDialogTitle>
                <DialogContent dividers>
                    <Typography gutterBottom>
                        You scored {props.playerScoreTotal} points while the AI scored {props.aiScoreTotal} points.
                    </Typography>
                    <Typography gutterBottom>
                        Praesent commodo cursus magna, vel scelerisque nisl consectetur et.
                        Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor.
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button autoFocus onClick={handleClose}>
                        New Game
                    </Button>
                </DialogActions>
            </BootstrapDialog>
        </div>
    );
}
