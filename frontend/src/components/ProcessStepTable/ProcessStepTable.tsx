import { useState } from "react";
import {
  Typography,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableRow,
  TableHead,
  Paper,
} from "@mui/material";

import { ProcessStepData } from "./ProcessStepData";
import { ProcessStepTableProps } from "./ProcessStepTableProps";

export function ProcessStepTable({
  productDetail,
  onInputChange,
  index,
}: ProcessStepTableProps): JSX.Element {
  const typeOfProcessStep = ["FE", "bumping", "sort", "DPS", "DC"];
  const [processStepDataList, setProcessStepDataList] = useState<
    ProcessStepData[]
  >([
    { step: "FE", cycleTime: 0, transitTime: 0, yield: 0 },
    { step: "bumping", cycleTime: 0, transitTime: 0, yield: 0 },
    { step: "sort", cycleTime: 0, transitTime: 0, yield: 0 },
    { step: "DPS", cycleTime: 0, transitTime: 0, yield: 0 },
    { step: "DC", cycleTime: 0, transitTime: 0, yield: 0 },
  ]);

  return (
    <Paper>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Process Step</TableCell>
            <TableCell>Cycle Time</TableCell>
            <TableCell>Transit Time</TableCell>
            <TableCell>Yield</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {processStepDataList.map((_item, rowIndex) => (
            <TableRow
              key={`process-step-row-${index}-${typeOfProcessStep[rowIndex]}`}
            >
              <TableCell>
                <Typography>{typeOfProcessStep[rowIndex]}</Typography>
              </TableCell>
              <TableCell>
                <TextField
                  id={`process-step-${index}-${typeOfProcessStep[rowIndex]}-ct`}
                  label="Cycle time"
                  value={productDetail.processStepData[rowIndex].cycleTime}
                  onChange={(e) => {
                    const newProcessStepData = [...processStepDataList];
                    newProcessStepData[rowIndex].cycleTime = Number(
                      e.target.value
                    );
                    setProcessStepDataList(newProcessStepData);
                    onInputChange("processStepData", newProcessStepData);
                  }}
                />
              </TableCell>
              <TableCell>
                <TextField
                  id={`process-step-${index}-${typeOfProcessStep[rowIndex]}-tt`}
                  label="Transit time"
                  value={productDetail.processStepData[rowIndex].transitTime}
                  onChange={(e) => {
                    const newProcessStepData = [...processStepDataList];
                    newProcessStepData[rowIndex].transitTime = Number(
                      e.target.value
                    );
                    setProcessStepDataList(newProcessStepData);
                    onInputChange("processStepData", newProcessStepData);
                  }}
                />
              </TableCell>
              <TableCell>
                <TextField
                  id={`process-step-${index}s-${typeOfProcessStep[rowIndex]}-yield`}
                  label="Yield"
                  value={productDetail.processStepData[rowIndex].yield}
                  onChange={(e) => {
                    const newProcessStepData = [...processStepDataList];
                    newProcessStepData[rowIndex].yield = Number(e.target.value);
                    setProcessStepDataList(newProcessStepData);
                    onInputChange("processStepData", newProcessStepData);
                  }}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
}
