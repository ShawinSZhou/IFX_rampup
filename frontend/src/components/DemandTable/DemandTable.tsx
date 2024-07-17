import React from "react";
import { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableRow,
  Paper,
  Typography,
  MenuItem,
} from "@mui/material";
import {
  eachWeekOfInterval,
  eachMonthOfInterval,
  eachQuarterOfInterval,
  addWeeks,
  addMonths,
  addQuarters,
  startOfYear,
} from "date-fns";
import { DemandTableProps } from "./DemandTableProps";
import { DemandData } from "./DemandData";
import { ProductDetails } from "../ProductDetailTab/ProductDetails";
import { Key } from "@mui/icons-material";

export const DemandTable: React.FC<DemandTableProps> = ({
  productDetail,
  onInputChange,
  index,
}: DemandTableProps) => {
  // Define state for timescale and from/to dates
  const [timescale, setTimescale] = useState<string>("");
  const [fromYear, setFromYear] = useState<number | "">("");
  const [fromTime, setFromTime] = useState<number | "">("");
  const [toYear, setToYear] = useState<number | "">("");
  const [toTime, setToTime] = useState<number | "">("");
  const [demandTime, setDemandTime] = useState<string[]>([]);
  const [demandQuantity, setDemandQuantity] = useState<number[]>([]);
  const [demandDataList, setDemandDataList] = useState<DemandData[]>([]);

  const handleNumberInputChange = (
    value: string,
    setState: React.Dispatch<React.SetStateAction<number | "">>
  ) => {
    setState(value ? Number(value) : "");
  };

  const createIntervalArray = (
    startDate: Date,
    endDate: Date,
    timescale: string
  ): Date[] => {
    switch (timescale) {
      case "week":
        return eachWeekOfInterval({ start: startDate, end: endDate });
      case "month":
        return eachMonthOfInterval({ start: startDate, end: endDate });
      case "quarter":
        return eachQuarterOfInterval({ start: startDate, end: endDate });
      default:
        return [];
    }
  };

  // Function to generate the demand time intervals
  const generateTimeIntervals = () => {
    if (!fromYear || !fromTime || !toYear || !toTime || !timescale) return;
    const startIndex = typeof fromTime === "number" ? fromTime - 1 : 0;
    const endIndex = typeof toTime === "number" ? toTime - 1 : 0;
    const startDate = {
      year: typeof fromYear === "number" ? fromYear : new Date().getFullYear(),
      index: startIndex,
    };
    const endDate = {
      year: typeof toYear === "number" ? toYear : new Date().getFullYear(),
      index: endIndex,
    };

    // Generate the intervals
    const intervals = createIntervalArray(
      timescale === "week"
        ? addWeeks(startOfYear(new Date(startDate.year, 0)), startDate.index)
        : timescale === "month"
        ? addMonths(startOfYear(new Date(startDate.year, 0)), startDate.index)
        : addQuarters(
            startOfYear(new Date(startDate.year, 0)),
            startDate.index
          ),
      timescale === "week"
        ? addWeeks(startOfYear(new Date(endDate.year, 0)), endDate.index)
        : timescale === "month"
        ? addMonths(startOfYear(new Date(endDate.year, 0)), endDate.index)
        : addQuarters(startOfYear(new Date(endDate.year, 0)), endDate.index),
      timescale
    );
    // Create labels for the intervals
    const intervalLabels = intervals.map((date: Date) => {
      const year = date.getFullYear();
      let formattedDate;
      switch (timescale) {
        case "week":
          const week = Math.ceil(
            (date.getTime() - startOfYear(date).getTime()) /
              (7 * 24 * 60 * 60 * 1000)
          );
          formattedDate = `${year}-W${week}`;
          break;
        case "month":
          formattedDate = new Intl.DateTimeFormat("en-US", {
            year: "numeric",
            month: "2-digit",
          }).format(date);
          break;
        case "quarter":
          const month = date.getMonth();
          const quarter = Math.floor(month / 3) + 1;
          formattedDate = `${year}-Q${quarter}`;
          break;
        default:
          formattedDate = "";
      }
      return formattedDate;
    });

    // Update demandDataList state
    const newDemandDataList = intervalLabels.map((label) => ({
      demandTime: label,
      demandQuantity: 0,
    }));
    setDemandDataList(newDemandDataList);

    // Update productDetail demandData using onInputChange
    onInputChange("demandData", newDemandDataList);
  };

  // Define timescales options
  const timescales = [
    { value: "quarter", label: "Quarter" },
    { value: "month", label: "Month" },
    { value: "week", label: "Week" },
  ];

  return (
    <Paper>
      {/* Render your timescale selection and date inputs */}
      <Grid container spacing={2}>
        <Grid item>
          <TextField
            id={`select-timescale-${index}`}
            select
            label="Select timescale"
            value={timescale}
            onChange={(e) => {
              setTimescale(e.target.value);
            }}
            helperText="Please select the timescale for your demand"
          >
            {timescales.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
        </Grid>
        {/* Timescale input fields */}
        <Grid item>
          <TextField
            id={`from-year-${index}`}
            label="From Year"
            type="number"
            value={fromYear}
            onChange={(e) =>
              handleNumberInputChange(e.target.value, setFromYear)
            }
          />
        </Grid>
        <Grid item>
          <TextField
            id={`from-time-${index}`}
            label={`From Time (${timescale})`}
            type="number"
            value={fromTime}
            onChange={(e) =>
              handleNumberInputChange(e.target.value, setFromTime)
            }
          />
        </Grid>
        <Grid item>
          <TextField
            id={`to-year-${index}`}
            label="To Year"
            type="number"
            value={toYear}
            onChange={(e) => handleNumberInputChange(e.target.value, setToYear)}
          />
        </Grid>
        <Grid item>
          <TextField
            id={`to-time-${index}`}
            label={`To Time (${timescale})`}
            type="number"
            value={toTime}
            onChange={(e) => handleNumberInputChange(e.target.value, setToTime)}
          />
          <Button
            variant="contained"
            onClick={(e) => {
              generateTimeIntervals();
            }}
          >
            Generate Demand Table
          </Button>
        </Grid>
      </Grid>

      {/* Demand table */}
      <Table>
        <TableBody>
          {productDetail?.demandData?.map(
            (
              item: {
                demandTime: string;
                demandQuantity: number;
              },
              rowIndex: number
            ) => (
              <TableRow key={rowIndex}>
                <TableCell>
                  <Typography>{item.demandTime}</Typography>
                </TableCell>
                <TableCell>
                  <TextField
                    id={`demand-quantity-${index}-${rowIndex}`}
                    label="Demand Quantity"
                    value={productDetail.demandData[rowIndex].demandQuantity}
                    onChange={(e) => {
                      const newDemandData = [...productDetail.demandData];
                      newDemandData[rowIndex].demandQuantity = Number(
                        e.target.value
                      );
                      onInputChange("demandData", newDemandData);
                    }}
                    type="number"
                  />
                </TableCell>
              </TableRow>
            )
          )}
        </TableBody>
      </Table>
    </Paper>
  );
};
