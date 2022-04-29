using System;
using System.ComponentModel;
using System.Linq;
using thumbnailService.Context;
using thumbnailService.Entities.Sql;
using thumbnailService.Models;

namespace thumbnailService.Converters;

public static class JobStatusConverter
{
    public static Guid ToGuid(this JobStatus input, ModelThumbnailDBContext context)
    {
        var converter = TypeDescriptor.GetConverter(typeof(JobStatus));
        var statusString = converter.ConvertToString(input);
        
        Jobstatus status = context.Jobstatus.FirstOrDefault(s => s.Name.Equals(statusString));
        if (status == null)
        {
            throw new NullReferenceException("Status not found!");
        }

        return status.Id;
    }
}
