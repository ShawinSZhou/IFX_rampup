// DemandTableContext.tsx
import React, { createContext, useState, useContext } from "react";

interface DemandTableContextProps {
  timescale: string;
  fromYear: number | "";
  fromTime: number | "";
  toYear: number | "";
  toTime: number | "";
  demandTime: string[];
  demandQuantity: number[];
  setTimescale: React.Dispatch<React.SetStateAction<string>>;
  setFromYear: React.Dispatch<React.SetStateAction<number | "">>;
  setFromTime: React.Dispatch<React.SetStateAction<number | "">>;
  setToYear: React.Dispatch<React.SetStateAction<number | "">>;
  setToTime: React.Dispatch<React.SetStateAction<number | "">>;
  setDemandTime: React.Dispatch<React.SetStateAction<string[]>>;
  setDemandQuantity: React.Dispatch<React.SetStateAction<number[]>>;
}

const DemandTableContext = createContext<DemandTableContextProps | null>(null);

export const useDemandTable = () => useContext(DemandTableContext)!;

export const DemandTableProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [timescale, setTimescale] = useState<string>("");
  const [fromYear, setFromYear] = useState<number | "">("");
  const [fromTime, setFromTime] = useState<number | "">("");
  const [toYear, setToYear] = useState<number | "">("");
  const [toTime, setToTime] = useState<number | "">("");
  const [demandTime, setDemandTime] = useState<string[]>([]);
  const [demandQuantity, setDemandQuantity] = useState<number[]>([]);

  return (
    <DemandTableContext.Provider
      value={{
        timescale,
        setTimescale,
        fromYear,
        setFromYear,
        fromTime,
        setFromTime,
        toYear,
        setToYear,
        toTime,
        setToTime,
        demandTime,
        setDemandTime,
        demandQuantity,
        setDemandQuantity,
      }}
    >
      {children}
    </DemandTableContext.Provider>
  );
};
