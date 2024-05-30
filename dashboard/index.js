import dotenv from "dotenv";
import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";
import { createClient } from "@supabase/supabase-js";

dotenv.config();
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => res.redirect("/dashboard.html"));

app.get("/alarm", async (req, res) => {
  let { data, error } = await supabase.from("alarms").select("*");

  if (error) {
    const errorObj = {
      status: "error",
      message: "Failed to fetch alarm timestamps",
    };

    res.status(500).send(errorObj);
  } else {
    const responseObj = {
      status: "success",
      data,
    };

    res.status(200).send(responseObj);
  }
});

app.post("/alarm", async (req, res) => {
  const { error } = await supabase.from("alarms").insert({}); // database is configured to automatically store current timestamp in newly created row

  if (error) {
    const errorObj = {
      status: "error",
      message: "Failed to record alarm",
    };

    res.status(500).send(errorObj);
  } else {
    const responseObj = {
      status: "success",
      message: "Recorded alarm successfully",
    };

    res.status(200).send(responseObj);
  }
});

app.get("/yawn", async (req, res) => {
  let { data, error } = await supabase.from("yawns").select("*");

  if (error) {
    const errorObj = {
      status: "error",
      message: "Failed to fetch yawn timestamps",
    };

    res.status(500).send(errorObj);
  } else {
    const responseObj = {
      status: "success",
      data,
    };

    res.status(200).send(responseObj);
  }
});

app.post("/yawn", async (req, res) => {
  const { error } = await supabase.from("yawns").insert({}); // database is configured to automatically store current timestamp in newly created row

  if (error) {
    const errorObj = {
      status: "error",
      message: "Failed to record yawn",
    };

    res.status(500).send(errorObj);
  } else {
    const responseObj = {
      status: "success",
      message: "Recorded yawn successfully",
    };

    res.status(200).send(responseObj);
  }
});

app.all("*", (req, res) => {
  const responseObj = {
    status: "error",
    message: "Invalid url",
  };

  res.status(404).send(responseObj);
});

app.listen(PORT, () => {
  console.log(`Listening at port ${PORT}`);
});

export default app;
