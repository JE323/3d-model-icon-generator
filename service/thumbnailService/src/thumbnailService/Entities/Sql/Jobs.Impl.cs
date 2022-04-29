﻿using System;
using System.Text.Json.Serialization;

namespace thumbnailService.Entities.Sql;

public partial class Jobs
{
    [JsonConstructor]
    public Jobs() { }

    public Jobs(Guid id, string name, Guid? modelid, Guid? statusid, Jobstatus status)
    {
        Id = id;
        Name = name;
        Modelid = modelid;
        Statusid = statusid;
    }

    public Jobs(string name, Guid? modelid, Guid? statusid, Jobstatus status)
    {
        Id = new Guid();
        Name = name;
        Modelid = modelid;
        Statusid = statusid;
    }
}