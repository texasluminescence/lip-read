from typing import Dict, Tuple

import torch
import torch.nn.functional as F
from torch import Tensor, nn


class Criterion(nn.Module):
    def __init__(self, loss_weights: Dict[str, float] = {}, blank_token: int = 0) -> None:
        super().__init__()

        self.loss_weights = loss_weights

        self.ctc_loss = nn.CTCLoss(blank=blank_token, zero_infinity=True) 

    def forward(self, predictions: Tuple[Tensor, Tensor], targets: Tuple[Tensor, Tensor]) -> Dict[str, Tensor]:
        """
        Args:
        predictions: (prediction_logits, input_lengths)
        targets: (targets, target_lengths)
        """ 
        ctc_loss = self._get_ctc_loss(predictions, targets)

        losses = {"ctc": ctc_loss}

        self._check_for_nans(losses)

        # The overall loss is a weighted combination of losses
        losses["overall"] = sum(losses[loss_name] * self.loss_weights.get(loss_name, 1) for loss_name in losses)

        return losses

    def _get_ctc_loss(self, predictions: Tuple[Tensor, Tensor], targets: Tuple[Tensor, Tensor]) -> Tensor:
        prediction_logits, input_lengths = predictions

        log_probabilities = F.log_softmax(prediction_logits, dim=2)

        # Pytorch expects predictions to be (T, B, C)
        log_probabilities = log_probabilities.permute(1, 0, 2)

        targets, target_lengths = targets

        ctc_loss = self.ctc_loss(log_probabilities, targets, input_lengths, target_lengths)

        return ctc_loss
    
    def __call__(self, *args) -> Dict[str, Tensor]:
        return super().__call__(*args)

    def _check_for_nans(self, losses: Dict[str, Tensor]) -> None:
        nan_losses = [name for name, loss in losses.items() if torch.isnan(loss).any()]

        if nan_losses:
            raise ValueError(f"NaNs detected in losses: {nan_losses}")